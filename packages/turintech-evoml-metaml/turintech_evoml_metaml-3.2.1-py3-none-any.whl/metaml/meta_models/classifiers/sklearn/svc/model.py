from sklearn.svm import SVC


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaSVCClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SVC(**self.params.internal_representation)
