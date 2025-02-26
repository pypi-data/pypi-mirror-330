from lightgbm import LGBMClassifier


from ..lgbm_classifier import LibLGBMClassifier
from .metadata import metadata
from .parameters import Params


class MetaLGBMClassifier(LibLGBMClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = LGBMClassifier(**self.params.internal_representation)
