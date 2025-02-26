from lightning.regression import FistaRegressor


from ..lightning_regressor import LibLightningRegressor
from .metadata import metadata
from .parameters import Params


class MetaFistaRegressor(LibLightningRegressor):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = FistaRegressor(**self.params.internal_representation)
