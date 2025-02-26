from sktime.forecasting.ets import AutoETS


from ..sktime_forecaster import LibSKTimeForecaster
from .metadata import metadata
from .parameters import Params


class MetaAutoETSForecaster(LibSKTimeForecaster):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = AutoETS(**self.params.internal_representation)
