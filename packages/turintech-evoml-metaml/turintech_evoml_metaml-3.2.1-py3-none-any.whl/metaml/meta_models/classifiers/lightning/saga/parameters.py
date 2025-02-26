from enum import Enum
from typing import Union


from metaml.meta_models.parameters import ParametersModel


class Eta(str, Enum):
    AUTO = "auto"
    LINE_SEARCH = "line-search"


class Loss(str, Enum):
    LOG = "log"
    SMOOTH_HINGE = "smooth_hinge"
    SQUARED_HINGE = "squared_hinge"


class Params(ParametersModel):
    eta: Union[Eta, float] = Eta.AUTO
    alpha: float = 1.0
    beta: float = 0.0
    loss: Loss = Loss.SMOOTH_HINGE
    gamma: float = 1.0
    max_iter: int = 10
    tol: float = 1e-3
