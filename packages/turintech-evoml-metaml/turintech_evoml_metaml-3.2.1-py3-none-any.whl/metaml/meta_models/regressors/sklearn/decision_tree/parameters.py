from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Criterion(str, Enum):
    ABSOLUTE_ERROR = "absolute_error"
    FRIEDMAN_MSE = "friedman_mse"
    SQUARED_ERROR = "squared_error"


class Splitter(str, Enum):
    BEST = "best"
    RANDOM = "random"


class Params(ParametersModel):
    criterion: Criterion = Criterion.SQUARED_ERROR
    splitter: Splitter = Splitter.BEST
    max_depth: int = 10
    min_samples_split: float = 1e-4
    min_samples_leaf: int = 1
    min_weight_fraction_leaf: float = 0.0
    max_leaf_nodes: int = 1000
    min_impurity_decrease: float = 0.0
    ccp_alpha: float = 0.0
