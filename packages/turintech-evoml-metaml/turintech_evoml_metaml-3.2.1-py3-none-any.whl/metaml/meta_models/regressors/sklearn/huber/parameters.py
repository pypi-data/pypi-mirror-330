from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    epsilon: float = 1.35
    max_iter: int = 100
    alpha: float = 0.0001
    warm_start: bool = False
    fit_intercept: bool = True
    tol: float = 1e-05
