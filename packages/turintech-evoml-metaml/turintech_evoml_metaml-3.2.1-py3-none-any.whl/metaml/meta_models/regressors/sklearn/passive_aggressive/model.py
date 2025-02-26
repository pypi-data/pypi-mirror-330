from sklearn.linear_model import PassiveAggressiveRegressor


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaPassiveAggressiveRegressor(LibSKLearnRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = PassiveAggressiveRegressor(**self.params.internal_representation)
