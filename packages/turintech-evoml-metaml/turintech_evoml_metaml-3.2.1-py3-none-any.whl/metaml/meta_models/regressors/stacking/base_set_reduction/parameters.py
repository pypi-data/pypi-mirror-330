from ..parameters import StackingParams
from metaml.meta_models.classifiers.stacking.utils import (
    BaseSetReducer,
    RelevanceMetricRegression,
)


class Params(StackingParams):
    base_reducer: BaseSetReducer = BaseSetReducer.mrmr
    relevance_metric: RelevanceMetricRegression = RelevanceMetricRegression.randomForest
