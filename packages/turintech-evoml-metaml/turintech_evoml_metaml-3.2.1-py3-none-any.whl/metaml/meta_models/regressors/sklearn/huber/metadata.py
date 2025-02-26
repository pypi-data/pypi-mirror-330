from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.huber_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description="Huber Regressor is a linear model optimizing the squared loss and the absolute loss for the samples controlled by the threshold.",
    advantages=["It is robust to outliers"],
    disadvantages=["It has problems with accuracy efficiency and stability"],
    prime=[],
    display_name="Huber Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
