from metaml.meta_models.classifiers.stacking.utils import (
    BaseSetReducer,
    RelevanceMetricClassification,
)
from ..parameters import StackingParams


class Params(StackingParams):
    base_reducer: BaseSetReducer = BaseSetReducer.mrmr
    relevance_metric: RelevanceMetricClassification = RelevanceMetricClassification.randomForest
