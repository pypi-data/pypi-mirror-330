import pandas as pd


from typing import Iterable


from metaml.meta_models.classifiers.meta_classifier import MetaClassifier


class LibLightningClassifier(MetaClassifier):
    def _fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) containing the features of each sample of
            training data.
            y (pd.Series): A series of shape (n_samples,) containing the target labels of the samples in X.

        """
        self.model.fit(X.to_numpy(), y.to_numpy())

    def _predict(self, X: pd.DataFrame) -> Iterable:
        return self.model.predict(X.to_numpy())

    def _predict_proba(self, X: pd.DataFrame) -> Iterable:
        return self.model.predict_proba(X.to_numpy())
