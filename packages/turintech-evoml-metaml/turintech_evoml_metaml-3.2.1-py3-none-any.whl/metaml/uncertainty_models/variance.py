import numpy as np
import pandas as pd
import logging
from typing import Sequence
from scipy.stats import norm

from metaml.meta_models.regressors.meta_regressor import MetaRegressor
from .base import UncertaintyModel

logger = logging.getLogger(__name__)


class Variance(UncertaintyModel):
    """
    Implementation of UncertaintyModel that predicts the variance of a normal distribution
    of our uncertainty.

    Attributes
    ----------
    variance_model : MetaRegressor
        A MetaRegressor model used to predict variances.
    """

    variance_model: MetaRegressor

    def __init__(self, variance_model: MetaRegressor):
        """
        Initialize a new instance of Variance.

        Args:
            variance_model (MetaRegressor): An instance of a MetaRegressor used to predict variances.
        """
        self.variance_model = variance_model

    def fit(self, X: pd.DataFrame, residuals: pd.Series) -> None:
        """
        Fit the model to the given training data and residuals.

        Args:
            X (pd.DataFrame): Dataframe of shape (n_samples, n_features) containing features of the training samples.
            residuals (pd.Series): Series of shape (n_samples,) containing the residuals of the samples in X.
        """
        self.mean_squared_residual = np.mean(residuals**2)
        self.variance_model.fit(X, residuals**2)

    def predict_interval(self, X: pd.DataFrame, quantiles: Sequence[float]) -> pd.DataFrame:
        """
        Obtain prediction intervals for the given features.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) providing features of samples which will be
            labelled.
            quantiles (Sequence[float]): Quantiles for prediction intervals.

        Returns:
            intervals (pd.DataFrame): Prediction intervals for the given samples.
        """
        # Compute variances
        variances = self.variance_model.predict(X)

        # Replace negative variances with mean squared residual and log warning
        negative_variance_mask = variances < 0
        if np.any(negative_variance_mask):
            logger.warning("Negative variances were predicted and replaced by the mean squared residual.")
            variances[negative_variance_mask] = self.mean_squared_residual

        # Use the normal distribution to get the quantiles
        quantile_values = norm.ppf(quantiles, loc=0.0, scale=np.sqrt(variances)[:, np.newaxis])

        return pd.DataFrame(
            data=quantile_values,
            index=X.index,
            columns=[f"quantile_{q}" for q in quantiles],
        )
