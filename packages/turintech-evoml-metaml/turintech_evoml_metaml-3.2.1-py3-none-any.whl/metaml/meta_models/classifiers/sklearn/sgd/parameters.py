from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    HINGE = "hinge"
    LOG = "log_loss"
    MODIFIED_HUBER = "modified_huber"
    SQUARED_HINGE = "squared_hinge"
    PERCEPTRON = "perceptron"
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


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Params(ParametersModel):
    loss: Loss = Loss.HINGE
    penalty: Penalty = Penalty.L2
    alpha: float = 1e-4
    l1_ratio: float = 0.15
    fit_intercept: bool = True
    max_iter: int = 1000
    tol: float = 1e-3
    shuffle: bool = True
    epsilon: float = 1e-1
    learning_rate: LearningRate = LearningRate.OPTIMAL
    eta0: float = 0.0
    power_t: float = 0.5
    early_stopping: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 5
    class_weight: Optional[ClassWeight] = None
    warm_start: bool = False
    average: bool = False
