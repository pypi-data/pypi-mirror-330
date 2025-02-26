from sklearnex.svm import SVC


from ..intelex_classifier import LibIntelexClassifier
from .metadata import metadata
from .parameters import Params


class MetaIntelexSVCClassifier(LibIntelexClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = SVC(**self.params.internal_representation)
