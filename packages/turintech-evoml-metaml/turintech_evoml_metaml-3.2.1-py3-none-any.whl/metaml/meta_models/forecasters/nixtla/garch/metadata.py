from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_garch_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    description="The GARCH Forecaster is a statistical model used for forecasting volatility in time series data. It is particularly useful when the variance of the error term is believed to be serially autocorrelated. This model is commonly used in financial and economic analyses to estimate volatility of returns for stocks, bonds, and market indices. It assumes the variance of the error term follows an autoregressive moving average process, enabling it to account for time-varying volatility in the data.",
    advantages=[
        "Captures Volatility Clustering: GARCH models are adept at capturing the 'volatility clustering' phenomena often observed in financial time series data, allowing for more accurate modeling and forecasting of financial markets.",
        "Explainability: GARCH models provide a theoretically sound framework for understanding volatility dynamics, which can be valuable for researchers and practitioners when interpreting the results.",
    ],
    disadvantages=[
        "Difficulty in selecting p and q Parameters: Choosing the correct lag orders (p and q) can be challenging and often requires domain expertise or model selection techniques, adding to the complexity of model deployment.",
        "Constant Mean Requirement: The model assumes that the mean of the time series is constant over the time period being considered, which may not hold true for all types of data, thereby affecting the model's accuracy.",
    ],
    prime=[],
    display_name="GARCH Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
