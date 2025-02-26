from enum import Enum
from typing import Optional, Union


from metaml.meta_models.parameters import ParametersModel


class Criterion(str, Enum):
    GINI = "gini"
    ENTROPY = "entropy"


class MaxFeatures(Enum):
    SQRT = "sqrt"
    LOG2 = "log2"


class ClassWeight(str, Enum):
    BALANCED = "balanced"
    BALANCED_SUBSAMPLE = "balanced_subsample"


class Params(ParametersModel):
    max_depth: int = 10
    min_samples_split: float = 1e-4
    max_samples: Optional[float] = 1.0
    criterion: Criterion = Criterion.GINI
    n_estimators: int = 100
    min_samples_leaf: float = 1e-4
    min_weight_fraction_leaf: float = 0.0
    max_features: Union[MaxFeatures, float] = MaxFeatures.SQRT
    max_leaf_nodes: Optional[int] = 1024
    min_impurity_decrease: float = 0.0
    ccp_alpha: float = 0.0
    bootstrap: bool = True
    class_weight: Optional[ClassWeight] = None
