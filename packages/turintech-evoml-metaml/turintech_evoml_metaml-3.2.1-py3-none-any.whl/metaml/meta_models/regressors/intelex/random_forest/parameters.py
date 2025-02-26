from typing import Optional, Union
from enum import Enum


from metaml.meta_models.parameters import (
    ParametersModel,
    OverridableParametersModel,
)


class Criterion(str, Enum):
    SQUARED_ERROR = "squared_error"
    ABSOLUTE_ERROR = "absolute_error"
    FRIEDMAN_MSE = "friedman_mse"
    POISSON = "poisson"


class OverridableParams(OverridableParametersModel):
    n_jobs: int = -1  # Number of jobs to run in parallel. -1 indicates the model should use all available processors.


class Params(ParametersModel):
    _overridable = OverridableParams

    n_jobs: int = -1
    n_estimators: int = 100
    criterion: Criterion = Criterion.SQUARED_ERROR
    max_depth: int = 10
    min_samples_split: int = 2
    min_samples_leaf: float = 0.0001
    min_weight_fraction_leaf: float = 0.0
    max_features: Union[float, str] = 1.0
    max_leaf_nodes: Optional[int] = None
    min_impurity_decrease: float = 0.0
    ccp_alpha: float = 0.0
    bootstrap: bool = True
    max_samples: Optional[float] = None
