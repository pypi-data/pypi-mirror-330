from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_arima_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster},
    description="ARIMA stands for AutoRegressive Integrated Moving Average. This model consists of three main components: AR (p), I (d), and MA (q). AR is the autoregressive component, I is the integrated component, and MA is the moving average component. Unlike the Auto ARIMA model, the ARIMA model does not automatically conduct a search over possible model parameters to select the best fit. This is best for users who want full control of the model.",
    advantages=[
        "Interpretability: ARIMA models are generally more interpretable than some complex machine learning models.",
        "Versatility: ARIMA is capable of modeling a wide range of time series data with different characteristics.",
        "Incorporation of trend and seasonality: The model can handle trend and seasonality in the time series data.",
    ],
    disadvantages=[
        "Stationarity assumption: ARIMA models assume that the time series is stationary. This might not be the case for all types of time series data.",
        "Manual tuning: Unlike Auto ARIMA, ARIMA requires manual specification of the model parameters, which can be a complex and time-consuming process.",
        "Predictive performance: While ARIMA can be effective, it might not always provide the best predictive performance compared to some machine learning models.",
        "Dependence on historical data: Like other time series forecasting models, ARIMA's performance heavily depends on the historical data used for training.",
    ],
    prime=[],
    display_name="ARIMA Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
