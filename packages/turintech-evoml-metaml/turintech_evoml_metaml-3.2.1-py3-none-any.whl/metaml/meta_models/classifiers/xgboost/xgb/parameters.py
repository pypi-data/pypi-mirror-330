from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class ProcessType(str, Enum):
    DEFAULT = "default"
    UPDATE = "update"


class Booster(str, Enum):
    GBTREE = "gbtree"
    DART = "dart"


class TreeMethod(str, Enum):
    AUTO = "auto"
    EXACT = "exact"
    APPROX = "approx"
    HIST = "hist"
    GPU_HIST = "gpu_hist"


class Params(ParametersModel):
    process_type: ProcessType = ProcessType.DEFAULT
    n_jobs: int = 1
    n_estimators: int = 100
    max_depth: int = 10
    learning_rate: Optional[float] = None
    booster: Booster = Booster.GBTREE
    tree_method: TreeMethod = TreeMethod.HIST
    gamma: float = 0.0
    min_child_weight: float = 1.0
    max_delta_step: float = 0.0
    subsample: float = 1.0
    colsample_bytree: float = 1.0
    colsample_bylevel: float = 1.0
    colsample_bynode: float = 1.0
    reg_alpha: float = 0.0
    reg_lambda: float = 0.0
    num_parallel_tree: int = 1
    scale_pos_weight: Optional[float] = None
    enable_categorical: bool = False
