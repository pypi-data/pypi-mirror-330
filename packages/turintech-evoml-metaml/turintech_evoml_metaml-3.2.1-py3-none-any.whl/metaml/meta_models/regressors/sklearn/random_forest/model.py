from sklearn.ensemble import RandomForestRegressor


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaRandomForestRegressor(LibSKLearnRegressor):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = RandomForestRegressor(**self.params.internal_representation)
