from lightning.classification import SAGAClassifier


from ..lightning_classifier import LibLightningClassifier
from .metadata import metadata
from .parameters import Params


class MetaSAGAClassifier(LibLightningClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SAGAClassifier(**self.params.internal_representation)

    def has_predict_proba(self) -> bool:
        """SAGA supports probabilities with log loss in binary classification. This flag indicates that probabilities
        are not always supported"""
        return False
