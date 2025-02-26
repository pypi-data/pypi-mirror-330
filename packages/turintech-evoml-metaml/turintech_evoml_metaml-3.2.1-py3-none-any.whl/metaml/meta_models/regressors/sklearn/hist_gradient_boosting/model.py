from sklearn.ensemble import HistGradientBoostingRegressor


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaHistGradientBoostingRegressor(LibSKLearnRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = HistGradientBoostingRegressor(**self.params.internal_representation)
