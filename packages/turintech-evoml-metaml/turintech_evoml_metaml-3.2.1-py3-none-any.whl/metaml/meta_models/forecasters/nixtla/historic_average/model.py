from ..nixtla_forecaster import LibNixtlaForecaster
from .metadata import metadata
from .parameters import Params


from statsforecast.models import HistoricAverage


class MetaNixtlaGarchForecaster(LibNixtlaForecaster):
    metadata = metadata
    params: Params
    model_class = HistoricAverage

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
