from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    SQUARED_ERROR = "squared_error"
    HUBER = "huber"
    EPSILON_INSENSITIVE = "epsilon_insensitive"
    SQUARED_EPSILON_INSENSITIVE = "squared_epsilon_insensitive"


class Penalty(str, Enum):
    L1 = "l1"
    L2 = "l2"
    ELASTICNET = "elasticnet"


class LearningRate(str, Enum):
    CONSTANT = "constant"
    OPTIMAL = "optimal"
    INVSCALING = "invscaling"
    ADAPTIVE = "adaptive"


class Params(ParametersModel):
    loss: Loss = Loss.SQUARED_ERROR
    penalty: Penalty = Penalty.L2
    alpha: float = 0.0001
    l1_ratio: float = 0.15
    fit_intercept: bool = True
    tol: float = 0.001
    max_iter: int = 1000
    shuffle: bool = True
    epsilon: float = 0.1
    learning_rate: LearningRate = LearningRate.INVSCALING
    eta0: float = 0.01
    power_t: float = 0.25
    early_stopping: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 5
    warm_start: bool = False
    average: bool = False
