from sklearn.ensemble import GradientBoostingClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaGradientBoostingClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = GradientBoostingClassifier(**self.params.internal_representation)
