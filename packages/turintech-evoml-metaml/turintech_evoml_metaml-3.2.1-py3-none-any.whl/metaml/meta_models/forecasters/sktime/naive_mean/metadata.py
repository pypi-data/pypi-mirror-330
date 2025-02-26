from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.naive_mean_forecaster,
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    model_type={ModelTypeEnum.baseline},
    description="The naive rolling mean forecaster provides a baseline forecast by predicting future values using a rolling mean of past values.",
    advantages=[
        "Can be used as a benchmark.",
        "Fast training time.",
        "Easy to understand and interpret.",
    ],
    disadvantages=[
        "Does not make use of exogenous features.",
        "Does not take into account seasonality.",
        "Does not look for any correlations or relationships in the data.",
    ],
    prime=[],
    display_name="Naive Forecaster: Rolling Mean",
    supports=Supports(probabilities=False, feature_importances=False),
)
