from enum import Enum
from typing import Union


from metaml.meta_models.parameters import ParametersModel


class Termination(str, Enum):
    VIOLATION_SUM = "violation_sum"
    VIOLATION_MAX = "violation_max"


class MaxSteps(str, Enum):
    AUTO = "auto"


class Selection(str, Enum):
    CYCLIC = "cyclic"
    UNIFORM = "uniform"


class Penalty(str, Enum):
    L1 = "l1"
    L2 = "l2"
    L1_L2 = "l1/l2"


class Loss(str, Enum):
    SQUARED_HINGE = "squared_hinge"
    LOG = "log"
    MODIFIED_HUBER = "modified_huber"
    SQUARED = "squared"


class Params(ParametersModel):
    C: float = 1.0
    alpha: float = 1.0
    max_iter: int = 50
    tol: float = 1e-3
    termination: Termination = Termination.VIOLATION_SUM
    shrinking: bool = True
    max_steps: Union[MaxSteps, int] = MaxSteps.AUTO
    sigma: float = 0.01
    beta: float = 0.5
    warm_start: bool = False
    debiasing: bool = False
    Cd: float = 1.0
    warm_debiasing: bool = False
    selection: Selection = Selection.CYCLIC
    permute: bool = True
    multiclass: bool = False
    penalty: Penalty = Penalty.L2
    loss: Loss = Loss.SQUARED_HINGE
