from sklearnex.linear_model import LogisticRegression


from ..intelex_classifier import LibIntelexClassifier
from .metadata import metadata
from .parameters import Params


class MetaIntelexLogisticRegressionClassifier(LibIntelexClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = LogisticRegression(**self.params.internal_representation)
