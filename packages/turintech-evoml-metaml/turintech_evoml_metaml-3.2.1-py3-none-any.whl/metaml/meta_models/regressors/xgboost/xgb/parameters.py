from typing import Optional
from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Booster(str, Enum):
    GBTREE = "gbtree"
    DART = "dart"


class TreeMethod(str, Enum):
    AUTO = "auto"
    EXACT = "exact"
    APPROX = "approx"
    HIST = "hist"
    GPU_HIST = "gpu_hist"


class ImportanceType(str, Enum):
    WEIGHT = "weight"
    COVER = "cover"
    GAIN = "gain"
    TOTAL_GAIN = "total_gain"
    TOTAL_COVER = "total_cover"


class Params(ParametersModel):
    n_estimators: int = 100
    max_depth: int = 10
    learning_rate: Optional[float] = None
    booster: Booster = Booster.GBTREE
    tree_method: TreeMethod = TreeMethod.HIST
    gamma: float = 0.0
    min_child_weight: float = 1.0
    max_delta_step: int = 0
    subsample: float = 1.0
    colsample_bytree: float = 1.0
    colsample_bylevel: float = 1.0
    colsample_bynode: float = 1.0
    reg_alpha: float = 0.0
    reg_lambda: float = 0.0
    num_parallel_tree: int = 1
    importance_type: ImportanceType = ImportanceType.GAIN
    enable_categorical: bool = False
