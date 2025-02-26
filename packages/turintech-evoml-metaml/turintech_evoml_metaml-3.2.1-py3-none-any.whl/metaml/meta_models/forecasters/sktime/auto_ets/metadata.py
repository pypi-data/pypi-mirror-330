from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.auto_ets_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    description="""ETS (Error, Trend, Seasonality) forecasting is a method of time series forecasting that decomposes a time series into three components:

Error: represents the random fluctuations or noise in the data, which cannot be explained by the trend or seasonality.

Trend: represents the overall direction (upward or downward) of the time series

Seasonality: represents the periodic fluctuations in the time series (e.g. monthly, quarterly, annually)

There are several variations of the ETS forecasting method, including ETS(A,N,N) (additive error, no trend, no seasonality), ETS(M,N,N) (multiplicative error, no trend, no seasonality), and ETS(A,A,N) (additive error and trend, no seasonality). These variations are used depending on the characteristics of the time series data. 

The <a href="https://www.sktime.org/en/stable/api_reference/auto_generated/sktime.forecasting.ets.AutoETS.html" target="_blank">AutoETS</a> model automatically chooses these hyperparameters including also damping of trend, and transformation of the data, among other things, by using the <a href="https://en.wikipedia.org/wiki/Akaike_information_criterion" target="_blank">Akaike Information Criterion (AIC)</a>. If you know the seasonality of your data, please fix it to the desired value, otherwise, make it tunable. Note by default the model assumes no seasonality in the data. For example, if you make the model tunable, it may determine that a time series of monthly sales data has a linear trend, a quarterly seasonality, and a Gaussian error term, and use these hyperparameters to generate forecasts.""",
    advantages=[
        "Robust",
        "Widely used",
        "Explainable",
        "May produce forecasts from noisy data",
    ],
    disadvantages=["Forecasts lag behind the actual trend"],
    prime=[],
    display_name="Auto ETS",
    supports=Supports(probabilities=False, feature_importances=False),
)
