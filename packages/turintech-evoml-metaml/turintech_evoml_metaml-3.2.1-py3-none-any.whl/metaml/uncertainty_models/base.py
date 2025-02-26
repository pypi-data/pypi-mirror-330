from abc import ABC, abstractmethod
from typing import Sequence
import pandas as pd


class UncertaintyModel(ABC):
    """
    Abstract base class representing an uncertainty model that can be added to a MetaRegressor.
    The UncertaintyModel should implement the `fit` and `predict_interval` methods.
    """

    @abstractmethod
    def fit(self, X: pd.DataFrame, residuals: pd.Series) -> None:
        """
        Abstract method for fitting the UncertaintyModel to a calibration dataset.

        The calibration dataset consists of features (X) and the residuals between
        the model's predictions and the actual values on the calibration set.

        Parameters
        ----------
        X : pd.DataFrame
            A DataFrame containing features.
        residuals : pd.Series
            A Series representing the difference between the model's predictions and the actual values.

        Returns
        -------
        None
        """
        ...

    @abstractmethod
    def predict_interval(self, X: pd.DataFrame, quantiles: Sequence[float]) -> pd.DataFrame:
        """
        Abstract method for obtaining prediction intervals at specified quantiles for new data.

        Parameters
        ----------
        X : pd.DataFrame
            A DataFrame containing features for which to compute prediction intervals.
        quantiles : Sequence[float]
            A sequence of floats representing the desired quantiles at which to compute prediction intervals.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the prediction intervals at the specified quantiles.
        """
        ...
