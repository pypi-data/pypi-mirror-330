from ..nixtla_forecaster import LibNixtlaForecaster
from .metadata import metadata
from .parameters import Params


from statsforecast.models import GARCH


class MetaNixtlaGarchForecaster(LibNixtlaForecaster):
    metadata = metadata
    params: Params
    model_class = GARCH

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
