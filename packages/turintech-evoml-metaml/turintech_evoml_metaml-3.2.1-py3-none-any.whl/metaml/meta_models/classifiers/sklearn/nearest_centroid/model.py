from sklearn.neighbors import NearestCentroid


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaNearestCentroidClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = NearestCentroid(**self.params.internal_representation)
