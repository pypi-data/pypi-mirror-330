from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.median_dummy_regressor,
    model_type={ModelTypeEnum.baseline},
    tags={ModelTag.regressor},
    description="The median dummy regressor always predicts the median of the training set.",
    advantages=[
        "Easily explainable.",
        "Fast to train.",
        "Provides a baseline with which to compare other models.",
    ],
    disadvantages=["Ignores all feature information."],
    prime=[],
    display_name="Median Dummy Regressor",
    supports=Supports(probabilities=False, feature_importances=False),
)
