from typing import Optional, Any
from sktime.forecasting.naive import NaiveForecaster


from ..sktime_forecaster import LibSKTimeForecaster
from .metadata import metadata
from .parameters import Params


class MetaNaiveLastForecaster(LibSKTimeForecaster):
    metadata = metadata
    fitted_freq: Optional[Any]

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = NaiveForecaster(**self.params.internal_representation, strategy="last", window_length=None)
