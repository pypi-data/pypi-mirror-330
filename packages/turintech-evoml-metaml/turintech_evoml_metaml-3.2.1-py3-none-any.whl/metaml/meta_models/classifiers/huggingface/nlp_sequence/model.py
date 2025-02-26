from __future__ import annotations
import logging
import pandas as pd
import numpy as np
import shutil
import pickle
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    BatchEncoding,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    TextClassificationPipeline,
    pipeline,
)
from datasets import Dataset
from pathlib import Path
from typing import Union, Optional, List, Dict, Mapping, Any
from tempfile import TemporaryDirectory


from metaml._util.hf_callback import LoggingCallback
from metaml.exceptions import IOException
from metaml.exceptions import HugsLoadException
from ..huggingface_classifier import LibHuggingfaceClassifier
from .metadata import metadata
from .parameters import Params, HuggingFaceModelName, Device, HugsModelName


logger = logging.getLogger("metaml")


PARAMS_FILE_NAME = "params.json"  # Name of the file where the parameters are stored when using `load_from_dir`.
STR_COLUMNS_FILE_NAME = "str_columns.pkl"
HUGS_DIRECTORY = "/tmp/hugs"  # Directory where the hugs models are stored.


class NlpSequenceClassifier(LibHuggingfaceClassifier):
    """
    A classifier for sequence classification tasks using Transformer models from the Hugging Face library.

    This class creates a pipeline for tokenizing, training, and making predictions with Transformer models
    for classification tasks. The models can either be obtained from Hugging Face's model hub or a local directory
    with a pretrained model.

    Attributes:
        metadata (Metadata): A Metadata object providing additional metadata about the model and its training
        params (Params): An object that encapsulates all the model's configuration parameters
        model_name (Union[HuggingFaceModelName, HugsModelName]): The name of the transformer model to use
        num_labels (int): The number of class labels for the classification task
        use_gpu (bool): A flag indicating whether to use a GPU for training and prediction
        model (PreTrainedModel): The transformer model used for sequence classification
        tokenizer (PreTrainedTokenizerBase): The tokenizer used to preprocess the text data for the transformer model
        _str_cols (List[str]): A list of the columns in the training DataFrame that contain string data to be tokenized

    Args:
        path (Optional[Path], optional): Path to a pre-trained model. Defaults to None.
        **kwargs: Additional keyword arguments for model configuration

    Raises:
        HugsLoadException: If the model directory does not exist

    """

    metadata = metadata
    params: Params
    model_name: Union[HuggingFaceModelName, HugsModelName]
    num_labels: int
    use_gpu: bool
    model: PreTrainedModel
    _str_cols: List[str] = []
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast]
    _tokenizer_kwargs: Dict[str, Any]

    def __init__(self, path: Optional[Path] = None, **kwargs):
        """
        Initialize an instance of NlpSequenceClassifier.

        Args:
            path (Optional[Path], optional): Path to a pre-trained model. Defaults to None.
            **kwargs: Additional keyword arguments for model configuration.
        """
        self.params = Params(**kwargs)
        self.use_gpu = self.params.device == Device.GPU

        # We must construct model_name_or_path to load the transformer and tokenizer.
        model_name_or_path: Union[str, Path]
        if path is not None:
            model_name_or_path = path
        elif isinstance(self.params.model, HuggingFaceModelName):
            # If the model is a HuggingFaceModelName then we will
            # download it from the internet using the model name.
            model_name_or_path = self.params.model.value
        else:
            # Otherwise self.params.model is a string, and we expect to find the model in the HUGS_DIRECTORY.
            model_name_or_path = Path(HUGS_DIRECTORY) / self.params.model
            if not model_name_or_path.is_dir():
                raise HugsLoadException(f"The model directory does not exist: {model_name_or_path}.")

        # Initialize the tokenizer and model.
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path,
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name_or_path,
            output_attentions=False,
            output_hidden_states=False,
        )

        # Some models (e.g. gpt2) do not have a pad token. This must be added in order to perform batched training.
        if self.tokenizer.pad_token is None:
            pad_token = "<PAD>"
            self.tokenizer.add_special_tokens({"pad_token": pad_token})

            # We must communicate the new pad token to the model.
            self.model.config.pad_token_id = self.tokenizer.pad_token_id

            # We must resize the embeddings to include the new pad token, since it was trained without it.
            self.model.resize_token_embeddings(len(self.tokenizer))

        # Record the number of class labels expected by the model.
        # This will be automatically updated during fitting if necessary.
        self.num_labels = self.model.config.num_labels

        no_cuda = self.params.device == Device.CPU
        self.trainer_args = TrainingArguments(
            save_strategy="no",  # We will save the model manually after training.
            learning_rate=self.params.learning_rate,
            per_device_train_batch_size=self.params.batch_size,
            per_device_eval_batch_size=self.params.batch_size,
            num_train_epochs=self.params.epochs,
            lr_scheduler_type=self.params.lr_scheduler_type.value,
            no_cuda=no_cuda,  # Control usage of GPU.
            warmup_ratio=self.params.warmup_ratio,
            logging_strategy="epoch",
            log_level="info",
            report_to=self.params.report_to.value,
            output_dir="./output",
        )

        self._tokenizer_kwargs: Dict[str, Any] = {
            "padding": "max_length",  # Pads sequences to the maximum length.
            "truncation": True,  # Truncates sequences to the maximum length.
            "max_length": self.params.max_length,  # The maximum length for a sequence.
            "return_attention_mask": True,  # Ensures the function returns the attention mask.
        }

    def tokenize(self, text: str, text_pair: Optional[str] = None) -> BatchEncoding:
        """
        Tokenizes the provided text(s) and returns an encoded representation suitable for use with transformer models.

        This method uses the tokenizer's `__call__` method to handle the tokenization, padding and truncation of the
        input. Padding and truncation are necessary so that the input sequences are all the same length. This is crucial
        for batched training, since the model expects all inputs to be the same size.

        Arguments:
        text (str): The first sequence. It is the primary text input for tokenization.
        text_pair (Optional[str]): The second sequence. If provided, the function will process both texts as a pair,
        which is required for tasks like sequence classification and question-answering.

        Returns:
        BatchEncoding: A dictionary-like object containing the following fields:
        - input_ids: list of token ids to represent each token in the input text. Each id corresponds to a token in the
         tokenizer's vocabulary.
        - token_type_ids: list of ids indicating the sequence to which the token belongs (0 for the first sequence, 1
        for the second). This is useful for differentiating between the two sequences when `text_pair` is provided.
        - attention_mask (optional): list of indices (0 or 1) specifying which tokens should be attended to by the
        transformer model. Generally, it is 1 for all input tokens and 0 for all padding tokens.
        """
        return self.tokenizer(
            text=text,
            text_pair=text_pair,
            **self._tokenizer_kwargs,
        )

    def _validate_and_prepare_training_data(self, X: pd.DataFrame, y: pd.Series) -> Dataset:
        """
        Prepares the input data for training by tokenizing the text data and packaging it in a Dataset object.

        This method first identifies string columns in the input DataFrame X, selects these columns, and ensures all
        entries in these columns are non-empty strings. It then constructs a Dataset object from the DataFrame. If the
        DataFrame has two string columns, they are treated as pairs of sequences (for tasks like text-to-text
        translation or question answering).

        Args:
            X (pd.DataFrame): The DataFrame containing the text data for training.
            y (pd.Series): The labels corresponding to the text data.

        Returns:
            Dataset: A Dataset object containing the tokenized text data and corresponding labels.

        Raises:
            ValueError: If the number of string columns in X is not 1 or 2, or if any entry in the string columns
            is not a non-empty string.
        """

        # Identify string columns in X
        self._str_cols = X.select_dtypes(include=[object]).columns

        # If the number of string columns is not 1 or 2, raise an exception
        if len(self._str_cols) not in (1, 2):
            raise ValueError(f"Number of string columns in X must be 1 or 2, got {len(self._str_cols)}")

        if len(self._str_cols) == 1:
            data = pd.concat([X[self._str_cols[0]], y], axis=1)
            data.columns = ["text", "labels"]
        else:
            data = pd.concat([X[self._str_cols[0]], X[self._str_cols[1]], y], axis=1)
            data.columns = ["text", "text_pair", "labels"]

        data = Dataset.from_pandas(data)

        def parse_tokenize(batch: Mapping) -> BatchEncoding:
            """Selects the text and text_pair columns from the batch and tokenizes them."""
            text_pair = batch["text_pair"] if "text_pair" in batch else None
            return self.tokenize(text=batch["text"], text_pair=text_pair)

        data = data.map(parse_tokenize, batched=True)

        return data

    def _fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Trains the model on the provided input data.

        The method checks if the number of unique labels in the data matches the number of labels expected by the model.
        If there is a mismatch, the model is reinitialized with the correct number of labels. Finally, a Trainer object
        is created and used to train the model.

        Args:
            X (pd.DataFrame): The DataFrame containing the text data for training.
            y (pd.Series): The labels corresponding to the text data.

        Note:
            If the number of labels in the dataset is different from the number of labels expected by the model,
            the model is reinitialized with the correct number of labels.
        """
        data = self._validate_and_prepare_training_data(X, y)

        logger.info(
            "Training model nlp_sequence_classifier:"
            # f" model={self.model_name_or_path}"
            f" no_cuda={self.trainer_args.no_cuda}"
            f" device={self.params.device}"
        )

        num_labels = len(set(data["labels"]))

        # If the number of labels in the dataset is different from the number of labels expected by the model then we
        # have to change the classifier head. The safest way to do this is to reinitialize the model, specify the number
        # of labels and set ignore_mismatched_sizes=True.
        if num_labels != self.num_labels:
            # We save the model to a temporary directory and then reload it with the correct number of labels.
            with TemporaryDirectory() as tmpdir:
                self.model.save_pretrained(tmpdir)
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    pretrained_model_name_or_path=tmpdir,
                    num_labels=num_labels,
                    output_attentions=False,
                    output_hidden_states=False,
                    ignore_mismatched_sizes=True,
                )
            # Record the new number of labels.
            self.num_labels = num_labels

        trainer = Trainer(
            self.model.train(),
            self.trainer_args,
            train_dataset=data,
            callbacks=[LoggingCallback()],
        )
        _ = trainer.train()

    def _validate_and_prepare_prediction_input(self, X: pd.DataFrame) -> List[Dict[str, str]]:
        """
        Validates the input DataFrame for prediction and prepares it for the prediction pipeline.

        This method identifies the string columns in the DataFrame X and checks if they match the string columns
        used during training (_fit). It then prepares the input data for the prediction pipeline.

        Args:
            X (pd.DataFrame): The DataFrame containing the text data for prediction. This DataFrame should have one
            or two string columns.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing the text (and optionally text pair) for
            prediction.

        Raises:
            ValueError: If the string columns in X do not match the string columns used during fitting.
        """
        # Identify string columns in X
        str_cols = X.select_dtypes(include=[object]).columns

        # Check if the string columns are the same as in _fit
        if not np.array_equal(str_cols, self._str_cols):
            raise ValueError(
                "The string columns in X during prediction must be the same and in the same order as during fitting."
            )

        # prepare input for predict_pipeline
        if len(str_cols) == 1:
            return [{"text": x} for x in X[str_cols[0]].tolist()]
        else:
            return [{"text": x, "text_pair": y} for x, y in zip(X[str_cols[0]].tolist(), X[str_cols[1]].tolist())]

    def _create_predict_pipeline(self, return_all_scores=False) -> TextClassificationPipeline:
        """
        Creates a pipeline for text classification prediction.

        Args:
            return_all_scores (bool, optional): Whether to return scores for all classes. Defaults to False.

        Returns:
            pipeline: The prediction pipeline.
        """
        text_classification_pipeline = pipeline(
            task="text-classification",
            model=self.model.eval(),  # switch to evaluation mode (e.g. turn off dropout)
            tokenizer=self.tokenizer,
            device=self.model.device,
            return_all_scores=return_all_scores,
            **self._tokenizer_kwargs,
        )
        if not isinstance(text_classification_pipeline, TextClassificationPipeline):
            raise ValueError("The pipeline must be a TextClassificationPipeline.")
        return text_classification_pipeline

    def _predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Predicts the class labels for the provided input data.

        This method validates and prepares the input data using _validate_and_prepare_prediction_input, creates
        a prediction pipeline, and makes predictions using this pipeline. The predicted labels are converted from
        strings to integers using the label2id mapping from the model's configuration.

        Args:
            X (pd.DataFrame): The DataFrame containing the text data for prediction.

        Returns:
            pd.Series: A Series containing the predicted labels as integers, with the same index as X.
        """
        # Validate and prepare the input data
        input_data = self._validate_and_prepare_prediction_input(X)

        # Create prediction pipeline
        predict_pipeline = self._create_predict_pipeline(return_all_scores=False)

        # Obtain predictions
        predictions = predict_pipeline(input_data)

        # Obtain the predicted labels as integers
        predicted_ids = [self.model.config.label2id[p["label"]] for p in predictions]

        return pd.Series(predicted_ids, index=X.index, name="prediction")

    def _predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Predicts the class probabilities for the provided input data.

        This method validates and prepares the input data using _validate_and_prepare_prediction_input, creates
        a prediction pipeline, and makes predictions using this pipeline. It then extracts the probabilities from
        the predictions and returns them as a DataFrame.

        Args:
            X (pd.DataFrame): The DataFrame containing the text data for prediction.

        Returns:
            pd.DataFrame: A DataFrame containing the predicted probabilities for each class, with the same index as X.
        """
        # Validate and prepare the input data
        input_data = self._validate_and_prepare_prediction_input(X)

        # Create prediction pipeline with return_all_scores=True
        predict_proba_pipeline = self._create_predict_pipeline(return_all_scores=True)

        # Obtain predictions
        predictions = predict_proba_pipeline(input_data)

        # Obtain the predicted probabilities
        predicted_probs = []
        for row in predictions:
            predicted_probs_row = [p["score"] for p in row]
            predicted_probs.append(predicted_probs_row)

        return pd.DataFrame(predicted_probs, index=X.index)

    def has_predict_proba(self) -> bool:
        return True

    def save_to_dir(self, dirpath: Union[str, Path]) -> None:
        """Save the model to a directory. The directory will be created if it does not exist. We will save the
        transformer model, the tokenizer and the parameters used to initialize the model.

        Args:
            dirpath (Union[str, Path]): The directory to which the model will be saved.

        """
        dirpath = Path(dirpath)

        # Save the transformer model and tokenizer.
        self.model.save_pretrained(dirpath)
        self.tokenizer.save_pretrained(dirpath)

        # Save the parameters.
        params_path = dirpath / PARAMS_FILE_NAME
        params_path.write_text(self.params.json())

        # Save _str_cols
        str_columns_path = dirpath / STR_COLUMNS_FILE_NAME
        with str_columns_path.open("wb") as f:
            pickle.dump(self._str_cols, f)

    @classmethod
    def load_from_dir(cls, dirpath: Union[str, Path]) -> NlpSequenceClassifier:
        """Load the model from a directory. The directory must contain the transformer model and the tokenizer. If the
        directory contains the parameters then these will be used to initialize the model, otherwise we will use the
        default parameters."""
        directory_path: Path = Path(dirpath)
        if not directory_path.is_dir():
            raise IOException(f'Directory "{directory_path}" does not exist.')

        # Load the parameters or use the defaults.
        params_path = directory_path / PARAMS_FILE_NAME
        params = Params.parse_file(params_path).dict() if params_path.exists() else Params().dict()

        # Load _str_cols
        str_columns_path = directory_path / STR_COLUMNS_FILE_NAME
        with str_columns_path.open("rb") as f:
            str_columns = pickle.load(f)

        # Initialize the model.
        model = cls(path=directory_path, **params)
        model._str_cols = str_columns
        return model

    def save(self, dirpath: Union[str, Path]) -> Path:
        """Save the model to a zip file.

        Args:
            dirpath (Union[str, Path]): The path to the directory where "model.zip" will be saved.

        Returns:
            Path: The path to the saved zip file.

        """
        directory_path: Path = Path(dirpath)
        if not directory_path.exists():
            raise IOException(f'Directory "{directory_path}" does not exist.')

        # We need the filename without the extension to pass to shutil.make_archive.
        filepath_without_extension: str = str(directory_path / "model")

        # We save the model to a temporary directory and then zip it.
        with TemporaryDirectory() as tmpdir:
            self.save_to_dir(tmpdir)
            shutil.make_archive(base_name=filepath_without_extension, format="zip", root_dir=tmpdir)

        return Path(filepath_without_extension).with_suffix(".zip")

    @classmethod
    def load(cls, dirpath: Union[str, Path]) -> NlpSequenceClassifier:
        """Load the model from a zip file.

        Args:
            dirpath (Union[str, Path]): The path to the directory where "model.zip" is saved.


        Returns:
            NlpSequenceClassifier: The model.

        """
        directory_path: Path = Path(dirpath)
        if not directory_path.is_dir():
            raise IOException(f'Directory "{directory_path}" does not exist.')

        filepath = directory_path / "model.zip"
        if not filepath.is_file():
            raise IOException(f'File "{filepath}" does not exist.')

        # We unpack the zip file to a temporary directory and then load the model from it.
        with TemporaryDirectory() as tmpdir:
            shutil.unpack_archive(filepath, tmpdir, format="zip")
            return cls.load_from_dir(tmpdir)
