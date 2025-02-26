from lightning.classification import SVRGClassifier


from ..lightning_classifier import LibLightningClassifier
from .metadata import metadata
from .parameters import Params


class MetaSVRGClassifier(LibLightningClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SVRGClassifier(**self.params.internal_representation)

    def has_predict_proba(self) -> bool:
        """This model only supports probabilities for binary classification with the modified Huber or log loss
        functions."""
        return False
