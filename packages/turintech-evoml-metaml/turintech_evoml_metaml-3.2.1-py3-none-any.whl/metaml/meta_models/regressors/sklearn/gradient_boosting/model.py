from sklearn.ensemble import GradientBoostingRegressor


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaGradientBoostingRegressor(LibSKLearnRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = GradientBoostingRegressor(**self.params.internal_representation)
