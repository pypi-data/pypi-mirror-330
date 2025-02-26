import pandas as pd


from typing import Iterable
from sklearn.base import BaseEstimator


from metaml.meta_models.regressors.meta_regressor import MetaRegressor


class LibIntelexRegressor(MetaRegressor):
    model: BaseEstimator

    def _fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) containing the features of each sample of
            training data.
            y (pd.Series): A series of shape (n_samples,) containing the target values of the samples in X.

        """
        self.model.fit(X, y)

    def _predict(self, X: pd.DataFrame) -> Iterable:
        return self.model.predict(X)
