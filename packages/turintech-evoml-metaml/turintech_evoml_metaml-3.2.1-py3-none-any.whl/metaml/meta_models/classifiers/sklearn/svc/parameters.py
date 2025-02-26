from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Kernel(str, Enum):
    LINEAR = "linear"
    POLY = "poly"
    RBF = "rbf"
    SIGMOID = "sigmoid"


class Gamma(str, Enum):
    SCALE = "scale"
    AUTO = "auto"


class DecisionFunctionShape(str, Enum):
    OVR = "ovr"
    OVO = "ovo"


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Params(ParametersModel):
    probability: bool = True
    C: float = 1.0
    kernel: Kernel = Kernel.RBF
    degree: int = 3
    gamma: Gamma = Gamma.SCALE
    coef0: float = 0.0
    shrinking: bool = True
    tol: float = 1e-3
    max_iter: int = 2000
    decision_function_shape: DecisionFunctionShape = DecisionFunctionShape.OVR
    break_ties: bool = False
    class_weight: Optional[ClassWeight] = None
