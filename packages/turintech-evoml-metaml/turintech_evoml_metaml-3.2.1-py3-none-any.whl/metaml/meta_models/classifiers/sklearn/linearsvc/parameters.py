from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class MultiClass(str, Enum):
    OVR = "ovr"
    CRAMMER_SINGER = "crammer_singer"


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Loss(str, Enum):
    HINGE = "hinge"
    SQUARED_HINGE = "squared_hinge"


class Penalty(str, Enum):
    L1 = "l1"
    L2 = "l2"


class Params(ParametersModel):
    tol: float = 1e-4
    C: float = 1.0
    multi_class: MultiClass = MultiClass.OVR
    fit_intercept: bool = True
    intercept_scaling: float = 1.0
    class_weight: Optional[ClassWeight] = None
    max_iter: int = 1000
    loss: Loss = Loss.SQUARED_HINGE
    dual: bool = True
    penalty: Penalty = Penalty.L2
