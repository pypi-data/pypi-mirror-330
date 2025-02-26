from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Penalty(str, Enum):
    L1 = "l1"
    L2 = "l2"
    ELASTICNET = "elasticnet"


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Params(ParametersModel):
    penalty: Optional[Penalty] = None
    alpha: float = 1e-4
    fit_intercept: bool = True
    max_iter: int = 1000
    tol: float = 1e-3
    shuffle: bool = True
    eta0: float = 1.0
    early_stopping: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 5
    class_weight: Optional[ClassWeight] = None
    warm_start: bool = False
