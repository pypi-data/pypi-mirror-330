from enum import Enum
from typing import Optional, Union
from metaml.meta_models.parameters import ParametersModel


class Criterion(str, Enum):
    GINI = "gini"
    ENTROPY = "entropy"


class Splitter(str, Enum):
    BEST = "best"
    RANDOM = "random"


class MaxFeatures(Enum):
    SQRT = "sqrt"
    LOG2 = "log2"


class ClassWeight(str, Enum):
    BALANCED = "balanced"


class Params(ParametersModel):
    criterion: Criterion = Criterion.GINI
    splitter: Splitter = Splitter.BEST
    max_depth: int = 10
    min_samples_split: float = 1e-4
    min_samples_leaf: int = 1
    min_weight_fraction_leaf: float = 0.0
    max_features: Union[MaxFeatures, float] = 1.0
    max_leaf_nodes: int = 1024
    min_impurity_decrease: float = 0.0
    ccp_alpha: float = 0.0
    class_weight: Optional[ClassWeight] = None
