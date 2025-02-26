from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Penalty(str, Enum):
    L1 = "l1"
    L2 = "l2"
    L1_L2 = "l1/l2"


class Termination(str, Enum):
    VIOLATION_SUM = "violation_sum"
    VIOLATION_MAX = "violation_max"


class Selection(str, Enum):
    UNIFORM = "uniform"
    CYCLIC = "cyclic"


class Params(ParametersModel):
    penalty: Penalty = Penalty.L2
    C: float = 1.0
    alpha: float = 1.0
    max_iter: int = 50
    tol: float = 1e-3
    termination: Termination = Termination.VIOLATION_SUM
    shrinking: bool = True
    max_steps: int = 30
    sigma: float = 0.01
    beta: float = 0.5
    warm_start: bool = False
    debiasing: bool = False
    Cd: float = 1.0
    warm_debiasing: bool = False
    selection: Selection = Selection.CYCLIC
    permute: bool = True
