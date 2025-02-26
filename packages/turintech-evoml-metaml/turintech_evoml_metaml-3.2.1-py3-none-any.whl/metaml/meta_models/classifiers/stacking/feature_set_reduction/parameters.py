from typing import Optional


from metaml._util.typing import strict
from ..utils import FeatureSetReducer, BaseSetReducer, RelevanceMetricClassification
from ..parameters import StackingParams


class Params(StackingParams):
    feature_reducers: strict(set, FeatureSetReducer) = {FeatureSetReducer.pca}
    base_reducer: Optional[BaseSetReducer] = BaseSetReducer.mrmr
    relevance_metric: RelevanceMetricClassification = RelevanceMetricClassification.fStatistic
    number_dimensions: int = 1
