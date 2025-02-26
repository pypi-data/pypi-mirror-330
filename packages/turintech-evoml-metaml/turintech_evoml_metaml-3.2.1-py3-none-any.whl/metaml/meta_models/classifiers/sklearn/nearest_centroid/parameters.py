from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Metric(str, Enum):
    EUCLIDEAN = "euclidean"


class Params(ParametersModel):
    metric: Metric = Metric.EUCLIDEAN
    shrink_threshold: Optional[float] = None
