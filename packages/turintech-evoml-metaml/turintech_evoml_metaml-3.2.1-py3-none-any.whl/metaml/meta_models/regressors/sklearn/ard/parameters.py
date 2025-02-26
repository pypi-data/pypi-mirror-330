from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    max_iter: int = 300
    tol: float = 1e-3
    alpha_1: float = 1e-6
    alpha_2: float = 1e-6
    lambda_1: float = 1e-6
    lambda_2: float = 1e-6
    threshold_lambda: float = 1e4
    fit_intercept: bool = True
