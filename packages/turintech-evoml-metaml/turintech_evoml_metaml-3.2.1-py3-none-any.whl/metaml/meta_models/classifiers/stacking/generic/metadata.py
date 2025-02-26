from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.stacking_classifier,
    model_type={ModelTypeEnum.ensemble},
    tags={ModelTag.classifier, ModelTag.experimental},
    description="A meta-classifier is fitted on the predictions of a number of base models, which may be combined with the initial training data.",
    advantages=[],
    disadvantages=[],
    prime=[],
    display_name="Stacking Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
