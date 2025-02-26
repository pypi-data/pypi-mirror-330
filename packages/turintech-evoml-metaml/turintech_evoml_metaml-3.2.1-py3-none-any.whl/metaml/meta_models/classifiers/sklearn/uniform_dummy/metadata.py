from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.uniform_dummy_classifier,
    model_type={ModelTypeEnum.baseline},
    tags={ModelTag.classifier},
    description="The uniform dummy classifier makes predictions by sampling from the distribution of the training class labels.",
    advantages=[
        "Easily explainable.",
        "Fast to train.",
        "Provides a reference with which to compare other models.",
    ],
    disadvantages=["Ignores all feature information.", "Poor performance."],
    prime=[],
    display_name="Uniform Dummy Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
