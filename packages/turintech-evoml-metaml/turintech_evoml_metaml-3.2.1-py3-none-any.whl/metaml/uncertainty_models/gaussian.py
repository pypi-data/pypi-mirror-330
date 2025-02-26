import numpy as np
import pandas as pd
from typing import Sequence
from scipy.stats import norm


from .base import UncertaintyModel


class StaticGaussian(UncertaintyModel):
    """
    Implementation of UncertaintyModel that assumes residuals follow a static Gaussian distribution.

    Attributes
    ----------
    mu : float
        The mean of the Gaussian distribution.
    sigma : float
        The standard deviation of the Gaussian distribution.
    """

    mu: float
    sigma: float

    def fit(self, X: pd.DataFrame, residuals: pd.Series) -> None:
        """
        Fit a normal distribution to the given residuals.

        Args:
            X (pd.DataFrame): Dataframe of shape (n_samples, n_features) containing features of the training samples.
            residuals (pd.Series): Series of shape (n_samples,) containing the residuals of the samples in X.
        """
        # fit a normal distribution to the residuals
        self.mu, self.sigma = norm.fit(residuals)

    def predict_interval(self, X: pd.DataFrame, quantiles: Sequence[float]) -> pd.DataFrame:
        """
        Obtain prediction intervals for the given features based on the fitted Gaussian distribution.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) providing features of samples which will be
            labelled.
            quantiles (Sequence[float]): Quantiles for prediction intervals.

        Returns:
            intervals (pd.DataFrame): Prediction intervals for the given samples, based on the quantiles of the fitted
            Gaussian distribution.
        """
        # Use the normal distribution to get the quantiles
        quantile_values = norm.ppf(quantiles, loc=self.mu, scale=self.sigma)

        # Repeat the quantiles for each prediction
        quantile_matrix = np.tile(quantile_values, (len(X), 1))

        return pd.DataFrame(
            data=quantile_matrix,
            index=X.index,
            columns=[f"quantile_{q}" for q in quantiles],
        )
