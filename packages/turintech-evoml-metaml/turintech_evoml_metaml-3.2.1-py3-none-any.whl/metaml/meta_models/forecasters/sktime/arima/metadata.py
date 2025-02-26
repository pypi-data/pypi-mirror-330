from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.arima_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    description="""The Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors (SARIMAX) model is a statistical model that can be used to analyze and forecast time series data that exhibits seasonal patterns and includes exogenous variables (variables that are not part of the time series we are forecasting).

A SARIMAX model is specified by seven parameters: p, d, q, P, D, Q and m. The p, d, and q parameters specify the order of the autoregressive term, the degree of differencing, and the order of the moving average term, respectively. The P, D, and Q parameters are similar, but are used to model the seasonal patterns in the data. Finally m specifies the number of time steps in a seasonal period.

In addition to these parameters, a SARIMAX model also includes one or more exogenous variables that are used to model the effects of external factors on the time series.""",
    advantages=[
        "Can handle non-stationary data. They can account for trends and seasonality in the data.",
        "Widely used and well-established, so there is a wide body of resources available for understanding and using these models.",
        "Simple and easy to implement.",
    ],
    disadvantages=["Can require significant computational resources to fit."],
    prime=[],
    display_name="SARIMAX",
    supports=Supports(probabilities=False, feature_importances=False),
)
