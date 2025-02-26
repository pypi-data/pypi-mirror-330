from enum import Enum
from typing import Optional, Union
from pydantic import validator


from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    DEVIANCE = "deviance"
    LOG_LOSS = "log_loss"
    EXPONENTIAL = "exponential"


class Criterion(str, Enum):
    FRIEDMAN_MSE = "friedman_mse"
    SQUARED_ERROR = "squared_error"


class MaxFeatures(Enum):
    SQRT = "sqrt"
    LOG2 = "log2"


class Params(ParametersModel):
    loss: Loss = Loss.LOG_LOSS
    learning_rate: float = 0.1
    n_estimators: int = 100
    subsample: float = 1.0
    criterion: Criterion = Criterion.FRIEDMAN_MSE
    min_samples_split: float = 0.0001
    min_samples_leaf: float = 0.0001
    min_weight_fraction_leaf: float = 0.0
    max_depth: int = 10
    min_impurity_decrease: float = 0.0
    max_features: Union[MaxFeatures, float] = 1.0
    max_leaf_nodes: int = 1024
    warm_start: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: Optional[int] = None
    tol: float = 1e-4
    ccp_alpha: float = 0.0

    @validator("loss", pre=True)
    def map_deviance_to_log_loss(cls, value):
        if value == Loss.DEVIANCE:
            return Loss.LOG_LOSS
        return value
