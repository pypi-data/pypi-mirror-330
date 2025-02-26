from enum import Enum


from metaml.meta_models.parameters import ParametersModel


class MultiClass(str, Enum):
    ONE_VS_REST = "one_vs_rest"
    ONE_VS_ONE = "one_vs_one"


class Params(ParametersModel):
    multi_class: MultiClass = MultiClass.ONE_VS_REST
    n_restarts_optimizer: int = 0
    max_iter_predict: int = 100
    warm_start: bool = False
