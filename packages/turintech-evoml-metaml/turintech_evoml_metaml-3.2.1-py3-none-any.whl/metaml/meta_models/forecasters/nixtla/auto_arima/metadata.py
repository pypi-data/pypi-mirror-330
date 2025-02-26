from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_auto_arima_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster},
    description="The Auto ARIMA forecaster an automated version of the ARIMA model, known for its ability to handle different types of time series data. Auto ARIMA works by conducting a search over possible model parameters to select the best fit that minimizes the AIC, BIC, or other user-defined criteria. It then uses the best parameters to generate forecasts. Auto ARIMA has the ability to incorporate seasonal patterns, trend, and other components into its model, making it a versatile tool for time series forecasting.",
    advantages=[
        "Automated model selection: Auto ARIMA automatically finds the best ARIMA model parameters, reducing the need for manual tuning.",
        "Versatility: Auto ARIMA is capable of modeling a wide range of time series data with different characteristics.",
        "Incorporation of seasonal patterns: The model can handle seasonality in the time series data.",
        "Interpretability: ARIMA models, including Auto ARIMA, are generally more interpretable than some complex machine learning models.",
    ],
    disadvantages=[
        "Stationarity assumption: ARIMA models assume that the time series is stationary. This might not be the case for all types of time series data.",
        "Computational intensity: The process of finding the best model parameters can be computationally intensive, especially for large datasets.",
        "Predictive performance: While Auto ARIMA can be effective, it might not always provide the best predictive performance compared to some machine learning models.",
        "Dependence on historical data: Like other time series forecasting models, Auto ARIMA's performance heavily depends on the historical data used for training.",
    ],
    prime=[],
    display_name="Auto ARIMA Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
