from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    EPSILON_INSENSITIVE = "epsilon_insensitive"
    SQUARED_EPSILON_INSENSITIVE = "squared_epsilon_insensitive"


class Params(ParametersModel):
    epsilon: float = 0.0
    tol: float = 1e-4
    C: float = 1.0
    fit_intercept: bool = True
    intercept_scaling: float = 1.0
    max_iter: int = 1000
    loss: Loss = Loss.SQUARED_EPSILON_INSENSITIVE
    dual: bool = True
