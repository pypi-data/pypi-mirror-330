from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class IC(str, Enum):
    AIC = "aic"
    AICC = "aicc"
    BIC = "bic"


class Params(ParametersModel):
    season_length: int = 1
    ic: IC = IC.AICC
