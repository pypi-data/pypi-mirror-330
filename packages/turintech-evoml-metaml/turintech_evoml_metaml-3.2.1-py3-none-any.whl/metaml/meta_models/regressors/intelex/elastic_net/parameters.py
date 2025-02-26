from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Selection(str, Enum):
    CYCLIC = "cyclic"
    RANDOM = "random"


class Params(ParametersModel):
    alpha: float = 1.0
    l1_ratio: float = 0.5
    fit_intercept: bool = True
    max_iter: int = 1000
    tol: float = 0.0001
    warm_start: bool = False
    positive: bool = False
    selection: Selection = Selection.CYCLIC
