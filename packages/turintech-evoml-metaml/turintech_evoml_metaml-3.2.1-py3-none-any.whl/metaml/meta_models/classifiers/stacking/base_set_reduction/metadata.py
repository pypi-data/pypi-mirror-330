from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.base_reduction_stacking_classifier,
    model_type={ModelTypeEnum.ensemble},
    tags={ModelTag.classifier, ModelTag.experimental},
    description="A meta-classifier is fitted on the predictions of a number of base models and the base predictions space is reduced to a lower dimensional space. It may be combined with the initial training data.",
    advantages=[],
    disadvantages=[],
    prime=[],
    display_name="Base Reduction Stacking Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
