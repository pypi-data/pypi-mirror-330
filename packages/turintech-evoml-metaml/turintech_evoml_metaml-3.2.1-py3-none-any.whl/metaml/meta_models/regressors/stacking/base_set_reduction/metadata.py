from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.base_reduction_stacking_regressor,
    model_type={ModelTypeEnum.ensemble},
    tags={ModelTag.regressor, ModelTag.experimental},
    description="A meta-regressor is fitted on the predictions of a number of base models and the base predictions space is reduced to a lower dimensional space. It may be combined with the initial training data.",
    advantages=[],
    disadvantages=[],
    prime=[],
    display_name="Base Reduction Stacking Regressor",
    supports=Supports(probabilities=False, feature_importances=False),
)
