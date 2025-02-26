from sklearn.tree import DecisionTreeClassifier


from ..sklearn_classifier import LibSKLearnClassifier
from .metadata import metadata
from .parameters import Params


class MetaDecisionTreeClassifier(LibSKLearnClassifier):
    metadata = metadata

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = DecisionTreeClassifier(**self.params.internal_representation)
