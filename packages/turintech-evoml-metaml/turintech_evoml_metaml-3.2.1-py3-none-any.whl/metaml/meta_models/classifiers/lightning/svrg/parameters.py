from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    MODIFIED_HUBER = "modified_huber"
    SMOOTH_HINGE = "smooth_hinge"
    SQUARED_HINGE = "squared_hinge"
    LOG = "log"
    SQUARED = "squared"


class Params(ParametersModel):
    eta: float = 1.0
    alpha: float = 1.0
    loss: Loss = Loss.SMOOTH_HINGE
    gamma: float = 1.0
    max_iter: int = 10
    n_inner: float = 1.0
    tol: float = 1e-3
