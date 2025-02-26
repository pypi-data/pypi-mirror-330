from lightning.classification import SDCAClassifier


from ..lightning_classifier import LibLightningClassifier
from .metadata import metadata
from .parameters import Params


class MetaSDCAClassifier(LibLightningClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SDCAClassifier(**self.params.internal_representation)

    def has_predict_proba(self) -> bool:
        return False
