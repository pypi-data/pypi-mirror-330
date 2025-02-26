from sklearn.svm import LinearSVC


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaLinearSVCClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = LinearSVC(**self.params.internal_representation)
