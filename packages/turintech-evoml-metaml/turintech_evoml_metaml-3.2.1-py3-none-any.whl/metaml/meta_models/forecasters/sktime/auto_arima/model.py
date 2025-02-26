from sktime.forecasting.arima import AutoARIMA


from ..sktime_forecaster import LibSKTimeForecaster
from .metadata import metadata
from .parameters import Params


class MetaAutoARIMAForecaster(LibSKTimeForecaster):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = AutoARIMA(**self.params.internal_representation)
