from typing import Optional, Union
from enum import Enum
from metaml.meta_models.parameters import ParametersModel, OverridableParametersModel


class Criterion(str, Enum):
    GINI = "gini"
    ENTROPY = "entropy"


class ClassWeight(str, Enum):
    BALANCED = "balanced"
    BALANCED_SUBSAMPLE = "balanced_subsample"


class OverridableParams(OverridableParametersModel):
    n_jobs: int = -1  # Number of jobs to run in parallel. -1 indicates the model should use all available processors.


class Params(ParametersModel):
    _overridable = OverridableParams

    n_jobs: int = -1
    n_estimators: int = 100
    criterion: Criterion = Criterion.GINI
    max_depth: int = 10
    min_samples_split: int = 2
    min_samples_leaf: float = 0.0001
    min_weight_fraction_leaf: float = 0.0
    max_features: Union[float, str] = "sqrt"
    max_leaf_nodes: Optional[int] = None
    min_impurity_decrease: float = 0.0
    class_weight: Optional[ClassWeight] = None
    ccp_alpha: float = 0.0
    bootstrap: bool = True
    max_samples: Optional[float] = None
