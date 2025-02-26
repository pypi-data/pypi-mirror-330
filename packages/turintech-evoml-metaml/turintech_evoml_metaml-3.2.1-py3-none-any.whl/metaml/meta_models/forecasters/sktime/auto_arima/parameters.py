from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class InformationCriterion(str, Enum):
    AIC = "aic"
    BIC = "bic"
    HQIC = "hqic"
    OOB = "oob"


class Params(ParametersModel):
    sp: int = 1
    information_criterion: InformationCriterion = InformationCriterion.AIC
