from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    EPSILON_INSENSITIVE = "epsilon_insensitive"
    SQUARED_EPSILON_INSENSITIVE = "squared_epsilon_insensitive"


class Params(ParametersModel):
    C: float = 1.0
    fit_intercept: bool = True
    max_iter: int = 1000
    tol: float = 0.001
    early_stopping: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 5
    shuffle: bool = True
    epsilon: float = 0.1
    loss: Loss = Loss.EPSILON_INSENSITIVE
    warm_start: bool = False
