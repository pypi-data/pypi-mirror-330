from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Penalty(str, Enum):
    L1 = "l1"
    L2 = "l2"
    ELASTICNET = "elasticnet"


class Solver(str, Enum):
    LIBLINEAR = "liblinear"
    SAG = "sag"
    SAGA = "saga"
    NEWTON_CG = "newton-cg"
    LBFGS = "lbfgs"


class MultiClass(str, Enum):
    AUTO = "auto"
    OVR = "ovr"
    MULTINOMIAL = "multinomial"


class Params(ParametersModel):
    tol: float = 1e-4
    C: float = 1.0
    fit_intercept: bool = True
    intercept_scaling: float = 1.0
    class_weight: Optional[ClassWeight] = None
    max_iter: int = 100
    warm_start: bool = False
    l1_ratio: Optional[float] = None
    dual: bool = False
    penalty: Optional[Penalty] = Penalty.L2
    solver: Solver = Solver.SAGA
    multi_class: MultiClass = MultiClass.AUTO
