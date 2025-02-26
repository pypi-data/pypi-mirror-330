from ..nixtla_forecaster import LibNixtlaForecaster
from .metadata import metadata
from .parameters import Params


from statsforecast.models import SeasonalNaive


class MetaNixtlaAutoArimaForecaster(LibNixtlaForecaster):
    metadata = metadata
    params: Params
    model_class = SeasonalNaive

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
