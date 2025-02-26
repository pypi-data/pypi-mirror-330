from enum import Enum
from typing import Optional
from metaml.meta_models.parameters import ParametersModel


class BoostingType(str, Enum):
    GBDT = "gbdt"
    RF = "rf"
    DART = "dart"
    GOSS = "goss"


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Params(ParametersModel):
    boosting_type: BoostingType = BoostingType.GBDT
    subsample: float = 0.9999
    subsample_freq: int = 0
    num_leaves: int = 31
    max_depth: int = 10
    learning_rate: float = 0.1
    n_estimators: int = 100
    subsample_for_bin: int = 200_000
    class_weight: Optional[ClassWeight] = None
    min_split_gain: float = 0.0
    min_child_weight: float = 1e-3
    min_child_samples: int = 20
    colsample_bytree: float = 1.0
    reg_alpha: float = 0.0
    reg_lambda: float = 0.0
