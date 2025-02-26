from catboost import CatBoostRegressor


from ..catboost_regressor import LibCatBoostRegressor
from .metadata import metadata
from .parameters import Params


class MetaCatBoostRegressor(LibCatBoostRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = CatBoostRegressor(**self.params.internal_representation)
