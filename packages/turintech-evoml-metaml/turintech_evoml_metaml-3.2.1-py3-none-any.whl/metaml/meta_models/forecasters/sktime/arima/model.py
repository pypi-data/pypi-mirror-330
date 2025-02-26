from sktime.forecasting.arima import ARIMA


from ..sktime_forecaster import LibSKTimeForecaster
from .metadata import metadata
from .parameters import Params


class MetaARIMAForecaster(LibSKTimeForecaster):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        params_internal_format = {
            "order": (self.params.p, self.params.d, self.params.q),
            "seasonal_order": (
                self.params.P,
                self.params.D,
                self.params.Q,
                self.params.sp,
            ),
        }
        self.model = ARIMA(**params_internal_format)
