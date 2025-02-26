from sklearnex.ensemble import RandomForestClassifier


from ..intelex_classifier import LibIntelexClassifier
from .metadata import metadata
from .parameters import Params


class MetaIntelexRandomForestClassifier(LibIntelexClassifier):
    metadata = metadata
    params: Params

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self.model = RandomForestClassifier(**self.params.internal_representation)
