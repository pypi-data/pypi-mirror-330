from sklearn.ensemble import ExtraTreesClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaExtraTreesClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = ExtraTreesClassifier(**self.params.internal_representation)
