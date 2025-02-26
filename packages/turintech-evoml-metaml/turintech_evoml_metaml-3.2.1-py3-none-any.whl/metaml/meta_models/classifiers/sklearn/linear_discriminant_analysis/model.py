from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaLinearDiscriminantAnalysisClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = LinearDiscriminantAnalysis(**self.params.internal_representation)
