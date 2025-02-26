from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    MODIFIED_HUBER = "modified_huber"
    HINGE = "hinge"
    SMOOTH_HINGE = "smooth_hinge"
    SQUARED_HINGE = "squared_hinge"
    PERCEPTRON = "perceptron"
    LOG = "log"
    SQUARED = "squared"


class Params(ParametersModel):
    eta: float = 1.0
    alpha: float = 1.0
    l1_ratio: float = 0.0
    loss: Loss = Loss.HINGE
    gamma: float = 1.0
    shuffle: bool = True
    n_iter: int = 10
