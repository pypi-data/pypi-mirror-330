from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    HINGE = "hinge"
    SQUARED_HINGE = "squared_hinge"


class ClassWeight(str, Enum):
    BALANCED = "balanced"
    NONE = "None"


class Params(ParametersModel):
    C: float = 1.0
    fit_intercept: bool = True
    max_iter: int = 1000
    tol: float = 0.001
    early_stopping: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 5
    shuffle: bool = True
    loss: Loss = Loss.HINGE
    warm_start: bool = False
    class_weight: Optional[ClassWeight] = None
    average: bool = False
