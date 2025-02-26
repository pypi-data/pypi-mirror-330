from lightning.regression import CDRegressor


from ..lightning_regressor import LibLightningRegressor
from .metadata import metadata
from .parameters import Params


class MetaCDRegressor(LibLightningRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = CDRegressor(**self.params.internal_representation)
