from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_seasonal_window_average_forecaster,
    model_type={ModelTypeEnum.baseline},
    tags=[ModelTag.ts, ModelTag.forecaster],
    description="The Window Average Forecaster is a model that uses the average of the last 'window_length' observations from the same period, where 'window_length' is the length of the window. Seasonality can also be captured by specifying the seasonal period.",
    advantages=[
        "Ability to capture seasonality: This model can capture seasonal variations by using the average of the last 'window_length' observations from the same period.",
        "Flexibility: The window length can be adjusted to focus on global or local trends.",
        "Simplicity: This model is straightforward to understand and implement, only requiring the calculation of the average of a number of past observations from the same period.",
    ],
    disadvantages=[
        "Lack of sophistication: This model does not consider any patterns or trends outside of the seasonal window in the data.",
        "Inaccuracy: The seasonal window average forecaster can be inaccurate if the data frequently changes or has a clear trend that extends beyond the seasonal window length.",
        "No consideration for recent changes: The model will not respond to recent changes in the data outside of the seasonal window.",
    ],
    prime=[],
    display_name="Window Average Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
