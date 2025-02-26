from xgboost import XGBClassifier

from ..xgboost_classifier import LibXGBoostClassifier
from .metadata import metadata
from .parameters import Params, TreeMethod


class MetaXGBClassifier(LibXGBoostClassifier):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.use_gpu = self.params.tree_method == TreeMethod.GPU_HIST
        self.model = XGBClassifier(**self.params.internal_representation)
