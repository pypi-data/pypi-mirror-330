from sklearn.ensemble import HistGradientBoostingClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaHistGradientBoostingClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = HistGradientBoostingClassifier(**self.params.internal_representation)
