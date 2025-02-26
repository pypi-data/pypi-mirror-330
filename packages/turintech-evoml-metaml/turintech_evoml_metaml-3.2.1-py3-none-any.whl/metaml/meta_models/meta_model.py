import pandas as pd
import numpy as np
import logging
import joblib


from typing import Dict, Any, Optional, Union
from abc import ABC, abstractmethod
from pathlib import Path


from metaml._util.utils import get_escaped_string
from metaml.meta_models.metadata import MetaData
from metaml.exceptions import IOException
from metaml.meta_models.parameters import ParametersModel


logger = logging.getLogger("metaml")


class MetaModel(ABC):
    """This is the parent class of all metamodels available in MetaML."""

    model: Optional[Any]
    metadata: MetaData
    params: ParametersModel
    input_params: Dict[str, Any] = {}
    use_gpu: bool = False  # Whether the model should use the GPU during fitting.

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model to the given training data.

        Args:
            X (pd.DataFrame): Features of the training data.
            y (pd.Series): Target vector.

        """

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Calculate model predictions.

        Args:
            X : array-like of shape (n_samples, n_features). Input data.
            **kwargs: Keyword arguments to be passed to the predict method of the wrapped model.

        Returns:
            Predictions of the target for the given features X.

        """

    @abstractmethod
    def has_predict_proba(self) -> bool:
        """Check if the model has a predict_proba method.

        Returns:
            True if the model has a predict_proba method, otherwise returns False.
        """

    def get_internal_params(self) -> Dict[str, Any]:
        """
        Retrieve internal parameters of our model, if they exist.

        Returns:
            Dict[str, Any]: Internal model parameters.
        """
        return {}

    @property
    def the_class(self) -> str:
        """Returns the name of the class."""
        return self.__class__.__name__

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        """Returns a string representation of the model."""
        signature = self.get_signature()
        return self.the_class + signature

    def get_signature(self) -> str:
        init_params = self.get_params(deep=False)
        signature = []
        for k, v in init_params.items():
            if isinstance(v, str):
                signature.append(k + "=" + "'" + get_escaped_string(v) + "'")
            elif v is np.nan:
                signature.append(k + "=np.nan")
            else:
                signature.append(k + "=" + str(v))
        joined_signature = ",\n ".join(signature)
        return f"({joined_signature})"

    def get_params(self, deep: int = True) -> Dict[str, Any]:
        """Retrieve a dictionary of the parameters used to initialise the MetaModel wrapper."""
        return self.params.external_representation

    def get_internal_model_params(self) -> Dict[str, Any]:
        """Retrieve a dictionary of the parameters used to initialise the internal model."""
        return self.params.internal_representation

    def get_input_params(self) -> Dict[str, Any]:
        """Retrieve a dictionary of the parameters supplied during instantiation of the MetaModel."""
        return self.input_params

    def set_input_params(self, input_params: Dict[str, Any]) -> None:
        """Saves parameters supplied during instantiation of the MetaModel, which are a subset of those found in
        self.params."""

        self.input_params = input_params

    @abstractmethod
    def score(self, X: pd.DataFrame, y_true: pd.Series) -> float:
        """Return the score of the performance of the trained model on supplied data.

        Args:
            X (pd.DataFrame): Features of the training data.
            y (pd.Series): Target vector.


        Returns:
            score (float): The score of the model on the supplied data.

        """
        ...

    def save(self, dirpath: Union[str, Path]) -> Path:
        """Save the model to disk. By default this will use joblib, but we expect this method to be overwritten when
        model specific saving methods are needed, e.g. for the NLPSequenceClassifier. The saved file will be called
        "model.joblib".

        Args:
            dirpath (Union[str, Path]): The path to the directory where "model.joblib" will be saved.

        Returns:
            Path: The path to the saved model.

        """
        dirpath = Path(dirpath)

        # Check if the directory exists
        if not dirpath.is_dir():
            raise IOException(f'The directory "{dirpath}" does not exist.')

        # Create the filepath
        filepath = dirpath / "model.joblib"

        # Save the model
        joblib.dump(self, filepath)

        return filepath

    @classmethod
    def load(cls, dirpath: Union[str, Path]) -> "MetaModel":
        """Load the model from disk. By default this will use joblib, but we expect this method to be overwritten when
        model specific loading methods are needed, e.g. for the NLPSequenceClassifier. The model is expected to be
        called "model.joblib".

        Args:
            dirpath (Union[str, Path]): The path to directory in which the "model.joblib" artifact will be found.

        Returns:
            MetaModel: The loaded model.

        """
        directory_path: Path = Path(dirpath)
        if not directory_path.is_dir():
            raise IOException(f'The directory "{directory_path}" does not exist.')

        filepath: Path = directory_path / "model.joblib"
        if not filepath.is_file():
            raise IOException(f'The file "{filepath}" does not exist.')

        return joblib.load(filepath)
