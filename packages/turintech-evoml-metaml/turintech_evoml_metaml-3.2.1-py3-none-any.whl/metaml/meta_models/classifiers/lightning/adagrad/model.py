from lightning.classification import AdaGradClassifier


from ..lightning_classifier import LibLightningClassifier
from .metadata import metadata
from .parameters import Params


class MetaAdaGradClassifier(LibLightningClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = AdaGradClassifier(**self.params.internal_representation)

    def has_predict_proba(self) -> bool:
        """Probabilities are supported for binary classification when we use log or modified huber loss."""
        return False
