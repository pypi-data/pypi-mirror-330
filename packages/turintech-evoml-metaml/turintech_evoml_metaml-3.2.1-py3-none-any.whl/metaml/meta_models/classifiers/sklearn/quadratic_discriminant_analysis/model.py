from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaQuadraticDiscriminantAnalysisClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = QuadraticDiscriminantAnalysis(**self.params.internal_representation)
