import pandas as pd


from typing import Iterable


from metaml.meta_models.regressors.meta_regressor import MetaRegressor


class LibCatBoostRegressor(MetaRegressor):
    def _fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) containing the features of each sample of
            training data.
            y (pd.Series): A series of shape (n_samples,) containing the target values of the samples in X.

        """
        # Find non-numeric columns
        cat_columns = X.select_dtypes(exclude="number").columns

        # Get the indices of the categorical columns
        cat_features = [X.columns.get_loc(col) for col in cat_columns]

        self.model.fit(X, y, cat_features=cat_features)

    def _predict(self, X: pd.DataFrame) -> Iterable:
        return self.model.predict(X)
