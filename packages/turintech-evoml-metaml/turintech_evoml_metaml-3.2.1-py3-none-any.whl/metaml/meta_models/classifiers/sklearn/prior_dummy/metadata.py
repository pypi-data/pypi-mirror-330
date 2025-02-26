from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.prior_dummy_classifier,
    model_type={ModelTypeEnum.baseline},
    tags={ModelTag.classifier},
    description="The prior dummy classifier always returns the most frequent class label from the training data. It's prediction probabilities match the class distribution of the training data.",
    advantages=[
        "Easily explainable.",
        "Fast to train.",
        "Provides a reference with which to compare other models.",
    ],
    disadvantages=["Ignores all feature information.", "Poor performance."],
    prime=[],
    display_name="Prior Dummy Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
