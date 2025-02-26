from sklearn.ensemble import RandomForestClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaRandomForestClassifier(LibSKLearnClassifier):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = RandomForestClassifier(**self.params.internal_representation)
