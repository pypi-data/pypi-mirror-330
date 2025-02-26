from sklearn.dummy import DummyClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaDummyClassifierPrior(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = DummyClassifier(strategy="prior")
