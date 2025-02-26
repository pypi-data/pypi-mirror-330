from lightgbm import LGBMRegressor


from ..lgbm_regressor import LibLGBMRegressor
from .metadata import metadata
from .parameters import Params


class MetaLGBMRegressor(LibLGBMRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = LGBMRegressor(**self.params.internal_representation)
