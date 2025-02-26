import pandas as pd


from ..stacking_classifier import LibStackingClassifier
from ..utils import StackingStrategy
from .metadata import metadata
from .parameters import Params


class MetaGenericStackingClassifier(LibStackingClassifier):
    """
    This is a Generic Stacking Model class
    derived from Base Stacking Model.
    """

    metadata = metadata
    params: Params

    def __init__(self, **kwargs) -> None:
        self.params = Params(**kwargs)
        super().__init__()

    def _stack_fit_transform(self, X: pd.DataFrame, X_base: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        # For combined stacking strategy we concat the initial training set
        # Otherwise we return X_base
        if self.params.strategy == StackingStrategy.combined:
            return pd.concat([X, X_base], axis=1)

        return X_base

    def _stack_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df_stack = self._get_base_predictions(X)

        if self.params.strategy == StackingStrategy.combined:
            df_stack = pd.concat([X, df_stack], axis=1)

        return df_stack
