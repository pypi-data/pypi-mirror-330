from enum import Enum
from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    SQUARED_ERROR = "squared_error"
    ABSOLUTE_ERROR = "absolute_error"
    HUBER = "huber"
    QUANTILE = "quantile"


class Criterion(str, Enum):
    FRIEDMAN_MSE = "friedman_mse"
    SQUARE_ERROR = "squared_error"


class Params(ParametersModel):
    loss: Loss = Loss.SQUARED_ERROR
    learning_rate: float = 0.1
    n_estimators: int = 100
    subsample: float = 1.0
    criterion: Criterion = Criterion.FRIEDMAN_MSE
    min_samples_split: float = 1e-4
    min_samples_leaf: float = 1e-4
    min_weight_fraction_leaf: float = 0.0
    max_depth: int = 10
    min_impurity_decrease: float = 0.0
    alpha: float = 0.9
    max_leaf_nodes: int = 10_000
    warm_start: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: Optional[int] = None
    tol: float = 1e-4
    ccp_alpha: float = 0.0
