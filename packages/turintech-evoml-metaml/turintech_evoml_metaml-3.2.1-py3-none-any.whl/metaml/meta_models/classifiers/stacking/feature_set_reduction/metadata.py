from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.feature_reduction_stacking_classifier,
    tags={ModelTag.classifier, ModelTag.experimental},
    model_type={ModelTypeEnum.ensemble},
    description="A meta-classifier is fitted on the predictions of a number of base models, which may be reduced to a lower dimensional space. It is combined with the initial training data, which is reduced to a lower dimensional space.",
    advantages=[],
    disadvantages=[],
    prime=[],
    display_name="Feature Reduction Stacking Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
