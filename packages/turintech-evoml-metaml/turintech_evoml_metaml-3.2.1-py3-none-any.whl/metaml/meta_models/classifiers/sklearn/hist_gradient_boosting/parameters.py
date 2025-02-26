from enum import Enum

from metaml.meta_models.parameters import ParametersModel


class Loss(str, Enum):
    AUTO = "auto"
    BINARY_CROSS_ENTROPY = "binary_crossentropy"
    CATEGORICAL_CROSS_ENTROPY = "categorical_crossentropy"


class Params(ParametersModel):
    loss: Loss = Loss.AUTO
    learning_rate: float = 0.1
    max_iter: int = 100
    max_leaf_nodes: int = 31
    max_depth: int = 10
    min_samples_leaf: int = 20
    l2_regularization: float = 0.0
    max_bins: int = 255
    warm_start: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: int = 10
    tol: float = 1e-07
