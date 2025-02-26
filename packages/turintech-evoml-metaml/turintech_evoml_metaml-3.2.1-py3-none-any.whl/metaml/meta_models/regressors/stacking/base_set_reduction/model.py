import pandas as pd
import logging


from mrmr import mrmr_regression


from ..stacking_regressor import LibStackingRegressor
from metaml.meta_models.classifiers.stacking.utils import (
    BaseSetReducer,
    RelevanceMetricRegression,
    StackingStrategy,
    calculate_number_features,
)
from .metadata import metadata
from .parameters import Params


logger = logging.getLogger("metaml")


class MetaBaseSetReductionStackingRegressor(LibStackingRegressor):
    """
    This is a Base Set Stacking Regression Model class
    derived from Base Stacking Model.

    Current implementations:
    1. Minimum Redundancy and Maximum Relevance (mRMR)
    2. ...

    """

    metadata = metadata
    params: Params

    def __init__(self, **kwargs) -> None:
        self.params = Params(**kwargs)
        super().__init__()

        # Base reducer validation
        if self.params.base_reducer not in list(BaseSetReducer):
            logger.error(f"Not valid base set reducer: {self.params.base_reducer}.")
            raise ValueError(f"Not valid base set reducer: {self.params.base_reducer}.")

        # Validate relevance metric
        if self.params.relevance_metric not in list(RelevanceMetricRegression):
            logger.error(f"Not valid relevance metric {self.params.relevance_metric}.")
            raise ValueError(f"Not valid relevance metric {self.params.relevance_metric}.")
        self.relevance_metric = self.params.relevance_metric

    def _stack_fit_transform(self, X: pd.DataFrame, X_base: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        # Reduce base models' predictions dataset using mrmr
        mrmr = mrmr_regression(
            X=X_base,
            y=y,
            K=calculate_number_features(X_base.shape[1]),
            return_scores=True,
            relevance=self.relevance_metric,
            show_progress=False,
        )

        # Update selected base models
        self.selected_base_models = mrmr[0]
        X_stack = X_base[self.selected_base_models]

        # For combined stacking strategy we concat the initial training set
        if self.params.strategy == StackingStrategy.combined:
            X_stack = pd.concat([X, X_stack], axis=1)

        return X_stack

    def _stack_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        # Get predictions for selected base models
        df_stack = self._get_base_predictions(X)

        # For combined stacking strategy we concat the initial training set
        if self.params.strategy == StackingStrategy.combined:
            df_stack = pd.concat([X, df_stack], axis=1)

        return df_stack
