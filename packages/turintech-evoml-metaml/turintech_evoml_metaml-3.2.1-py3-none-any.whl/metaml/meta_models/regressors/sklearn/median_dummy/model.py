from sklearn.dummy import DummyRegressor


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaMedianDummyRegressor(LibSKLearnRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = DummyRegressor(strategy="median")
