from typing import Union


from .utils import StackingStrategy
from metaml._util.typing import strict
from metaml.factory import factory
from metaml.meta_models.regressors.meta_regressor import MetaRegressor
from metaml.meta_models.names import RegressorName
from metaml.meta_models.parameters import ParametersModel


default_stacking_regressors = [
    factory.get_model(RegressorName.decision_tree_regressor),
    factory.get_model(RegressorName.linear_regressor),
]
default_stacking_meta_regressor = factory.get_model(RegressorName.elastic_net_regressor)


class StackingParams(ParametersModel):
    regressors: strict(list, MetaRegressor) = default_stacking_regressors
    meta_regressor: Union[MetaRegressor] = default_stacking_meta_regressor
    strategy: StackingStrategy = StackingStrategy.basic

    class Config:
        arbitrary_types_allowed = True
