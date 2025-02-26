from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    SQUARED_ERROR = "squared_error"
    ABSOLUTE_ERROR = "absolute_error"
    POISSON = "poisson"


class Params(ParametersModel):
    loss: Loss = Loss.SQUARED_ERROR
    learning_rate: float = 0.1
    max_iter: int = 100
    max_leaf_nodes: int = 31
    max_depth: int = 10
    min_samples_leaf: int = 20
    l2_regularization: float = 0.0
    max_bins: int = 255
    warm_start: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 10
    tol: float = 1e-4
