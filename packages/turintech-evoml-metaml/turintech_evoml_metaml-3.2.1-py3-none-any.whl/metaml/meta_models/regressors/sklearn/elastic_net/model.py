from sklearn.linear_model import ElasticNet


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaElasticNetRegressor(LibSKLearnRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = ElasticNet(**self.params.internal_representation)
