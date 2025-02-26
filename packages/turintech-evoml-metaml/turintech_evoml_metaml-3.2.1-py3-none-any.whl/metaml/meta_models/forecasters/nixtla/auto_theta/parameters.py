from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class DecompositionType(str, Enum):
    ADDITIVE = "additive"
    MULTIPLICATIVE = "multiplicative"


class Params(ParametersModel):
    season_length: int = 1
    decomposition_type: DecompositionType = DecompositionType.MULTIPLICATIVE
