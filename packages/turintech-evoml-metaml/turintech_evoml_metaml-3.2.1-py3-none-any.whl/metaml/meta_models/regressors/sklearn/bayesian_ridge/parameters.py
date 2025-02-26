from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    max_iter: int = 300
    tol: float = 1e-3
    alpha_1: float = 1e-6
    alpha_2: float = 1e-6
    lambda_1: float = 1e-6
    lambda_2: float = 1e-6
    alpha_init: Optional[float] = None
    lambda_init: float = None
    fit_intercept: bool = True
