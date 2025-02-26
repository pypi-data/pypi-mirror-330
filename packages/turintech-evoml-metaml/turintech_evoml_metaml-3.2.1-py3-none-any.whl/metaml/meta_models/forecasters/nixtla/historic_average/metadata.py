from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_historic_average_forecaster,
    model_type={ModelTypeEnum.baseline},
    tags=[ModelTag.ts, ModelTag.forecaster, ModelTag.experimental],
    description="The Historic Average Forecaster is a forecasting model that uses past data to predict future outcomes. By calculating the historic average of the given time series data, it provides a simple and straightforward forecast for future periods.",
    advantages=[
        "Simplicity: This model is easy to understand and implement.",
        "No need for additional data: Unlike other complex models, the historic average forecaster does not require additional variables or complex parameters for forecasting.",
        "Stability: Because it uses the average of past data, it provides a stable forecast, which is less sensitive to recent changes or fluctuations in the data.",
    ],
    disadvantages=[
        "Ignoring trends: This model assumes that the past will continue in the same way, which might not always be the case. It doesn't account for trends, seasonality, or other patterns in the data.",
        "No consideration for recent changes: The model might not respond quickly to recent changes in the data as it uses the average of all past data.",
        "Simplicity can be a drawback: Although its simplicity is an advantage, it can also be a drawback. For complex datasets with intricate patterns, the historic average forecaster might not provide the most accurate forecasts.",
    ],
    prime=[],
    display_name="Historic Average Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
