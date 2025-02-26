from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Penalty(str, Enum):
    L1 = "l1"
    L1_L2 = "l1/l2"
    TV1D = "tv1d"
    SIMPLEX = "simplex"


class Loss(str, Enum):
    SQUARED_HINGE = "squared_hinge"
    LOG = "log"
    LOG_MARGIN = "log_margin"


class Params(ParametersModel):
    penalty: Penalty = Penalty.L1
    C: float = 1.0
    alpha: float = 1.0
    max_iter: int = 100
    max_steps: int = 30
    sigma: float = 1e-5
    eta: float = 2.0
    multiclass: bool = False
    loss: Loss = Loss.SQUARED_HINGE
