from sklearnex.ensemble import RandomForestRegressor


from ..intelex_regressor import LibIntelexRegressor
from .metadata import metadata
from .parameters import Params


class MetaIntelexRandomForestRegressor(LibIntelexRegressor):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = RandomForestRegressor(**self.params.internal_representation)
