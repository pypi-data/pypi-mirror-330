from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Solver(str, Enum):
    AUTO = "auto"
    SVD = "svd"
    CHOLESKY = "cholesky"
    LSQR = "lsqr"
    SPARSE_CG = "sparse_cg"
    SAG = "sag"
    SAGA = "saga"
    LBFGS = "lbfgs"


class Params(ParametersModel):
    alpha: float = 1.0
    fit_intercept: bool = True
    max_iter: int = 1000
    positive: bool = False
    solver: Solver = Solver.AUTO
    tol: float = 0.0001
