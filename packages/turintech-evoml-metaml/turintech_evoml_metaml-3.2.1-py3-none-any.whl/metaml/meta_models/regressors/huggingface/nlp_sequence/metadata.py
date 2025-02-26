from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.nlp_sequence_regressor,
    model_type={ModelTypeEnum.deep_learning},
    tags={ModelTag.regressor, ModelTag.nlp},
    description="An NLP sequence regressor is a pretrained machine learning model that can be fine tuned to predict continuous values from sequences of text.",
    advantages=["Easy to use", "High accuracy"],
    disadvantages=["Slow training"],
    prime=["model"],
    display_name="NLP Sequence Regressor",
    supports=Supports(probabilities=False, feature_importances=False),
)
