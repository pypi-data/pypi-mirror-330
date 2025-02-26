from sklearn.linear_model import PassiveAggressiveClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaPassiveAgressiveClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = PassiveAggressiveClassifier(**self.params.internal_representation)
