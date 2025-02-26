from xgboost import XGBRegressor

from ..xgboost_regressor import LibXGBoostRegressor
from .metadata import metadata
from .parameters import Params, TreeMethod


class MetaXGBRegressor(LibXGBoostRegressor):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.use_gpu = self.params.tree_method == TreeMethod.GPU_HIST
        self.model = XGBRegressor(**self.params.internal_representation)
