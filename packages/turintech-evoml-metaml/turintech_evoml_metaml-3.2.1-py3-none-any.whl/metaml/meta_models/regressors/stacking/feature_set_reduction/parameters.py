from typing import Optional
from ..parameters import StackingParams


from metaml.meta_models.classifiers.stacking.utils import (
    FeatureSetReducer,
    BaseSetReducer,
    RelevanceMetricRegression,
)
from metaml._util.typing import strict


class Params(StackingParams):
    feature_reducers: strict(set, FeatureSetReducer) = {FeatureSetReducer.pca}
    base_reducer: Optional[BaseSetReducer] = BaseSetReducer.mrmr
    relevance_metric: RelevanceMetricRegression = RelevanceMetricRegression.fStatistic
    number_dimensions: int = 1
