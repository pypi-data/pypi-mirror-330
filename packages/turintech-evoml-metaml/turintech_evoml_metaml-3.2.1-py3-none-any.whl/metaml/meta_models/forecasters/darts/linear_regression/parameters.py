from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    lags: int = 5
    lags_past_covariates: int = 5
    lags_future_covariates: int = 1
    output_chunk_length: int = 5
    fit_intercept: bool = True
