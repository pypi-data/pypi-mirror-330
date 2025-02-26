from sklearnex.linear_model import LinearRegression


from ..intelex_regressor import LibIntelexRegressor
from .metadata import metadata
from .parameters import Params


class MetaIntelexLinearRegressor(LibIntelexRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = LinearRegression(**self.params.internal_representation)
