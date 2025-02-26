from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nixtla_auto_theta_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    description="The Auto Theta Model is a forecasting tool that automatically selects the most suitable Theta model variant for time series forecasting, based on Mean Squared Error (MSE). The Theta model, known for its effectiveness and simplicity, decomposes a time series into long-term and short-term components, making use of a parameter called theta to modify the local curvature of the series. The Auto Theta Model considers four different Theta models: the Standard Theta Model (STM), the Optimized Theta Model (OTM), the Dynamic Standard Theta Model (DSTM), and the Dynamic Optimized Theta Model (DOTM). By automatically selecting the best model among these, it provides an efficient way to generate accurate forecasts tailored to the specific characteristics of the given time series data.",
    advantages=[
        "Automated model selection: The Auto Theta Model automatically selects the best Theta model (STM, OTM, DSTM, DOTM) based on Mean Squared Error (MSE), eliminating the need for manual model selection and potentially improving forecast accuracy.",
        "Simplicity: Like the base Theta model, the Auto Theta Model is simple to implement and understand, making it accessible for users with varying degrees of expertise.",
        "Adaptability: The Auto Theta Model can adapt to different characteristics of the time series data by choosing the most appropriate Theta model variant.",
    ],
    disadvantages=[
        "Assumptions: The model implicitly assumes that the time series can be decomposed into stable components, is forecastable based on past data, and that the deseasonalized and detrended residuals are stationary, which may not hold true for all types of data.",
        "Overfitting: Since the Auto Theta Model selects the best model based on MSE, it may overfit to the training data and perform poorly on unseen data.",
        "Lack of control: While the Auto Theta Model's automatic model selection can be an advantage, it can also be a disadvantage for users who want more control over model selection and parameter tuning.",
    ],
    prime=[],
    display_name="Auto Theta Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
