from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_seasonal_naive_forecaster,
    model_type={ModelTypeEnum.baseline},
    tags=[ModelTag.ts, ModelTag.forecaster],
    description="The Naive Forecaster is a forecasting model that simply sets all forecasts to be the value of the last observation. This is the simplest method of forecasting, making no assumptions about the data and only using the last observed value to predict future outcomes. Seasonality can be incorporated by setting the `season_length` parameter.",
    advantages=[
        "Ability to capture seasonality: This model can capture seasonal variations by using the last known observation of the same period.",
        "Simplicity: This model is easy to understand and implement, only requiring the last observed value from the same season to make a prediction.",
    ],
    disadvantages=[
        "Lack of sophistication: This model does not consider any patterns or trends outside of seasonality in the data.",
        "Inaccuracy: The seasonal naive forecaster can be very inaccurate if the data frequently changes or has a clear trend outside of seasonality.",
        "No consideration for recent changes: The model will not respond to recent changes in the data, as it only uses the last observed value from the same season.",
    ],
    prime=[],
    display_name="Naive Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
