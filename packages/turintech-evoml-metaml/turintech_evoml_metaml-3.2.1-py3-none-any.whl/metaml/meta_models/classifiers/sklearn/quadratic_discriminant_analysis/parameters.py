from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    reg_param: float = 0.0
    store_covariance: bool = False
    tol: float = 1e-4
