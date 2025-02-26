from sklearnex.svm import SVR


from ..intelex_regressor import LibIntelexRegressor
from .metadata import metadata
from .parameters import Params


class MetaIntelexSVRRegressor(LibIntelexRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SVR(**self.params.internal_representation)
