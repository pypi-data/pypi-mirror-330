from sklearn.svm import SVR


from ..sklearn_regressor import LibSKLearnRegressor
from .metadata import metadata
from .parameters import Params


class MetaSVRRegressor(LibSKLearnRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SVR(**self.params.internal_representation)
