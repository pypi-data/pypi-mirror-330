from catboost import CatBoostClassifier


from ..catboost_classifier import LibCatBoostClassifier
from .metadata import metadata
from .parameters import Params


class MetaCatBoostClassifier(LibCatBoostClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = CatBoostClassifier(**self.params.internal_representation)
