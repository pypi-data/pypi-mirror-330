from ..nixtla_forecaster import LibNixtlaForecaster
from .metadata import metadata
from .parameters import Params


from statsforecast.models import AutoARIMA


class MetaNixtlaAutoArimaForecaster(LibNixtlaForecaster):
    metadata = metadata
    params: Params
    model_class = AutoARIMA

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
