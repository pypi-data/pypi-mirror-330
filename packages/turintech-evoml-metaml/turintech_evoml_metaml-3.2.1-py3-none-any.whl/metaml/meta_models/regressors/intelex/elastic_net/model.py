from sklearnex.linear_model import ElasticNet


from ..intelex_regressor import LibIntelexRegressor
from .metadata import metadata
from .parameters import Params


class MetaIntelexElasticNetRegressor(LibIntelexRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = ElasticNet(**self.params.internal_representation)
