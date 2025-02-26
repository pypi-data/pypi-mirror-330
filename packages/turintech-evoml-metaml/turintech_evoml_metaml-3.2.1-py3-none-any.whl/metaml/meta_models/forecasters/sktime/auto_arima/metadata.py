from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.auto_arima_forecaster,
    model_type={ModelTypeEnum.statistical},
    tags={ModelTag.ts, ModelTag.forecaster, ModelTag.experimental},
    description="""Auto SARIMAX is a machine learning model that can be used to automatically fit a Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors (SARIMAX) model to a time series. It is a variant of the SARIMAX model that uses an automated process to search for the optimal values of the model parameters, rather than requiring the user to specify these values manually.

Auto SARIMAX is often used when there is a need to quickly fit a SARIMAX model to a time series data set without extensive manual parameter tuning. It can be especially useful when working with large data sets or when there is limited time available to optimize the model parameters.

One of the main advantages of Auto SARIMAX is that it can significantly reduce the amount of time and effort required to fit a SARIMAX model to a time series data set.""",
    advantages=[
        "Automatically finds model parameters.",
        "Can handle non-stationary data. They can account for trends and seasonality in the data.",
        "Widely used and well-established, so there is a wide body of resources available for understanding and using these models.",
        "Simple and easy to implement.",
    ],
    disadvantages=[
        "Can require significant computational resources to fit.",
        "May not always find the optimal model parameters.",
    ],
    prime=[],
    display_name="Auto SARIMAX",
    supports=Supports(probabilities=False, feature_importances=False),
)
