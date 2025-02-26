from typing import Optional
from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class Solver(str, Enum):
    SVD = "svd"
    LSGR = "lsqr"
    EIGEN = "eigen"


class Params(ParametersModel):
    n_components: Optional[int] = None
    store_covariance: bool = False
    tol: float = 1e-4
    solver: Solver = Solver.SVD
    shrinkage: Optional[float] = None
