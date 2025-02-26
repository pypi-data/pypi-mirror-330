from lightning.classification import CDClassifier


from ..lightning_classifier import LibLightningClassifier
from .metadata import metadata
from .parameters import Params


class MetaCDClassifier(LibLightningClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = CDClassifier(**self.params.internal_representation)

    def has_predict_proba(self) -> bool:
        """Predict proba is flagged as not generally supported for this model. It may only be supported for certain
        parameters and scenarios (binary vs multiclass classification)."""
        return False
