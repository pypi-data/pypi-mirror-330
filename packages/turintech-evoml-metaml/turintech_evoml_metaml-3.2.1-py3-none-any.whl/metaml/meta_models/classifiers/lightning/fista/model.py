from lightning.classification import FistaClassifier

from ..lightning_classifier import LibLightningClassifier
from .metadata import metadata
from .parameters import Params


class MetaFistaClassifier(LibLightningClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = FistaClassifier(**self.params.internal_representation)

    def has_predict_proba(self) -> bool:
        return False
