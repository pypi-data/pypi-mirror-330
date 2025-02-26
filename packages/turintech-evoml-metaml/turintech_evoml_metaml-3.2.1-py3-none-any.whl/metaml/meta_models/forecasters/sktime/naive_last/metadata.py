from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.naive_last_forecaster,
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    model_type={ModelTypeEnum.baseline},
    description="The naive last value forecaster provides a baseline forecast by predicting future values using the previous values. A seasonal offset can be included.",
    advantages=[
        "Can be used as a benchmark.",
        "Fast training time.",
        "Easy to understand and interpret.",
    ],
    disadvantages=[
        "Does not make use of exogenous features.",
        "Does not look for any correlations or relationships in the data.",
    ],
    prime=[],
    display_name="Naive Forecaster: Last Value",
    supports=Supports(probabilities=False, feature_importances=False),
)
