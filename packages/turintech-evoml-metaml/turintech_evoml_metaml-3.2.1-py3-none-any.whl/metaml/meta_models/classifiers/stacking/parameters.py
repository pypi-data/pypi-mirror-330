from typing import Union


from .utils import StackingStrategy
from metaml.meta_models.classifiers.meta_classifier import MetaClassifier
from metaml.meta_models.names import ClassifierName
from metaml._util.typing import strict
from metaml.meta_models.parameters import ParametersModel
from metaml.factory import factory


default_stacking_classifiers = [
    factory.get_model(ClassifierName.logistic_regression_classifier),
    factory.get_model(ClassifierName.random_forest_classifier),
]
default_stacking_meta_classifier = factory.get_model(ClassifierName.random_forest_classifier)


class StackingParams(ParametersModel):
    classifiers: strict(list, MetaClassifier) = default_stacking_classifiers
    meta_classifier: Union[MetaClassifier] = default_stacking_meta_classifier
    strategy: StackingStrategy = StackingStrategy.basic

    class Config:
        arbitrary_types_allowed = True
