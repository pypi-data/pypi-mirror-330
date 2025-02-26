from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    SQUARED = "squared"
    ABSOLUTE = "absolute"
    HINGE = "hinge"
    SMOOTH_HINGE = "smooth_hinge"
    SQUARED_HINGE = "squared_hinge"


class Params(ParametersModel):
    loss: Loss = Loss.HINGE
    alpha: float = 1.0
    l1_ratio: float = 0.0
    gamma: float = 1.0
    max_iter: int = 100
    tol: float = 1e-3
