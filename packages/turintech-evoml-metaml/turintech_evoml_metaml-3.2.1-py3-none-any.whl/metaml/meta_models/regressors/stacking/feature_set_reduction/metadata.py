from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.feature_reduction_stacking_regressor,
    model_type={ModelTypeEnum.ensemble},
    tags={ModelTag.regressor, ModelTag.experimental},
    description="A meta-regressor is fitted on the predictions of a number of base models, which may be reduced to a lower dimensional space. It is combined with the initial training data, which is reduced to a lower dimensional space.",
    advantages=[],
    disadvantages=[],
    prime=[],
    display_name="Feature Reduction Stacking Regressor",
    supports=Supports(probabilities=False, feature_importances=False),
)
