import logging
import numpy as np
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from datasets import Dataset


from metaml._util.hf_callback import LoggingCallback
from ..huggingface_regressor import LibHuggingfaceRegressor
from .metadata import metadata
from .parameters import Params, Device


logger = logging.getLogger("metaml")


class NlpSequenceRegressor(LibHuggingfaceRegressor):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.use_gpu = self.params.device == Device.GPU
        self.batch_size = 32
        self.tokenizer = AutoTokenizer.from_pretrained(self.params.model.value, do_lower_case=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.params.model.value,
            output_attentions=False,
            output_hidden_states=False,
            num_labels=1,
        )

    def tokenize(self, input_text: str):
        """
        Returns <class transformers.tokenization_utils_base.BatchEncoding> with the following fields:
          - input_ids: list of token ids
          - token_type_ids: list of token type ids
          - attention_mask: list of indices (0,1) specifying which tokens should considered by the model (return_attention_mask = True).
        """
        return self.tokenizer(
            input_text,
            padding="max_length",
            truncation=True,
            max_length=self.params.max_length,
            return_attention_mask=True,
            return_tensors="pt",
        )

    def _fit(self, X: pd.DataFrame, y: pd.Series):
        y = y.astype(float)  # cast integers to float for model compatibilty

        data = pd.concat([X.iloc[:, 0], y], axis=1)
        data.columns = ["text", "labels"]
        data = Dataset.from_pandas(data)

        def tokenize(batch):
            return self.tokenize(batch["text"])

        data = data.map(tokenize, batched=True)

        no_cuda = self.params.device == Device.CPU

        logger.info(
            "Training model nlp_sequence_regressor:"
            f" model_name={self.params.model.value}"
            f" no_cuda={no_cuda}"
            f" device={self.params.device}"
        )

        self.trainer_args = TrainingArguments(
            f"checkpoint",
            save_strategy="no",
            learning_rate=self.params.learning_rate,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            num_train_epochs=self.params.epochs,
            log_level="error",
            report_to="none",
            no_cuda=no_cuda,
        )
        trainer = Trainer(
            self.model,
            self.trainer_args,
            train_dataset=data,
            tokenizer=self.tokenizer,
            callbacks=[LoggingCallback()],
        )
        _ = trainer.train()

    def _transform(self, X: pd.DataFrame) -> np.ndarray:
        data = X
        data.columns = ["text"]
        data = Dataset.from_pandas(data)

        def tokenize(batch):
            return self.tokenize(batch["text"])

        data = data.map(tokenize, batched=True)
        trainer = Trainer(self.model, self.trainer_args)
        raw_pred, _, _ = trainer.predict(data)
        return raw_pred

    def _predict(self, X: pd.DataFrame) -> np.ndarray:
        logits = self._transform(X)
        return logits.reshape(-1)
