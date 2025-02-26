import numpy as np
import pandas as pd


from abc import abstractmethod
from sklearn.metrics import accuracy_score


from metaml.meta_models.meta_model import MetaModel
from metaml.meta_models.metadata import ModelTag
from metaml.exceptions import PredictProbaException


class MetaClassifier(MetaModel):
    """This is the parent class for all classification meta-models available in MetaML"""

    _estimator_type: str = ModelTag.classifier

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit the model according to the given training data.

        Args:
            X (pd.DataFrame): dataframe of shape (n_samples, n_features) containing features of the training samples.
            y (pd.Series): series of shape (n_samples,) containing the labels of the samples in X.

        """

        self.classes_ = np.unique(y)
        self._fit(X, y)

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Obtain model predictions for the given features.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) providing features of samples which will be
             labelled.

        Returns:
            predictions (pd.Series): labels for the given samples.

        """
        return pd.Series(self._predict(X), index=X.index)

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Obtain probability estimates for predictions of classifier models.

        Args:
            X: array-like of shape (n_samples, n_features)
            Input data for prediction.

        Returns:
            array-like of shape (n_samples, n_classes)
            The probability of the sample for each class in the model.

        """
        if self.has_predict_proba():
            return pd.DataFrame(self._predict_proba(X), index=X.index)
        err_msg = f"This model {self.metadata.model_name} doesn't have predict_proba method."
        raise PredictProbaException(err_msg.format(self.metadata.model_name))

    def has_predict_proba(self) -> bool:
        """Check if the model has a predict_proba method.

        Returns:
            True if the model has a predict_proba method, otherwise returns False.
        """
        return bool(hasattr(self.model, "predict_proba"))

    def score(self, X: pd.DataFrame, y_true: pd.Series) -> float:
        """Return the accuracy score for the performance of the trained model on supplied data.

        Args:
            X (pd.DataFrame): Features of the training data.
            y (pd.Series): Target vector.


        Returns:
            score (float): The accuracy score of the model on the supplied data.

        """

        return accuracy_score(y_true, self.predict(X))

    @abstractmethod
    def _fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) containing the features of each sample of
            training data.
            y (pd.Series): A series of shape (n_samples,) containing the target labels of the samples in X.

        """
        """Library specific implementation of _fit for classification models."""

    @abstractmethod
    def _predict(self, X: pd.DataFrame) -> pd.Series:
        """Library specific implementation of _predict for classification models."""

    @abstractmethod
    def _predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """Library specific implementation of _predict_proba."""
