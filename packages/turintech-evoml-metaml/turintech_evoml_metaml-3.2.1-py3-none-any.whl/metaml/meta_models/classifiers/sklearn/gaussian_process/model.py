from sklearn.gaussian_process import GaussianProcessClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaGaussianProcessClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = GaussianProcessClassifier(**self.params.internal_representation)
