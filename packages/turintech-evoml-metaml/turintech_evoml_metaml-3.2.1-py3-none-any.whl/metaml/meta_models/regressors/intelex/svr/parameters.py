from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Kernel(str, Enum):
    POLY = "poly"
    RBF = "rbf"
    SIGMOID = "sigmoid"


class Params(ParametersModel):
    kernel: Kernel = Kernel.RBF
    degree: int = 3
    coef0: float = 0.0
    tol: float = 1e-3
    C: float = 1.0
    epsilon: float = 0.1
    shrinking: bool = True
    max_iter: int = 1000
