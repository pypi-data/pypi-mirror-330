from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_random_walk_with_drift_forecaster,
    model_type={ModelTypeEnum.baseline},
    tags=[ModelTag.ts, ModelTag.forecaster, ModelTag.experimental],
    description="The Random Walk with Drift Forecaster is a variation of the naive method that allows forecasts to change over time. The amount of change, referred to as drift, is calculated as the average change observed in the historical data. Essentially, this model is equivalent to drawing a line between the first and last observation and extrapolating this line to make future forecasts.",
    advantages=[
        "Ability to adapt: Unlike the naive method, this model allows forecasts to change over time, potentially providing better forecasts when there is a consistent trend in the data.",
        "Simplicity: This model is easy to understand and implement, only requiring the calculation of the average change in the historical data.",
    ],
    disadvantages=[
        "Assumption of linearity: This model assumes that the change over time is linear, which might not always be the case in real-world data.",
        "No consideration for sudden changes: The model might not respond quickly to sudden changes in the data as it uses the average change over all past data.",
    ],
    prime=[],
    display_name="Random Walk with Drift Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
