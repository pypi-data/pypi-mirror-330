from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.nbeats_forecaster,
    model_type={ModelTypeEnum.deep_learning},
    tags={ModelTag.ts, ModelTag.forecaster},
    description="The N-BEATS (Neural basis expansion analysis for interpretable time series forecasting) forecaster from the darts library is a state-of-the-art deep learning model designed to produce accurate and interpretable time series predictions. This model employs a unique combination of stacked fully connected layers and basis function expansion, which enables it to learn a diverse range of time series patterns. The architecture consists of two primary components: the backcast and forecast branches, both of which are designed to produce predictions for past and future time steps, respectively. The model's primary strength lies in its ability to learn interpretable components, which provide valuable insights into the underlying structure and characteristics of the time series data. N-BEATS has demonstrated exceptional performance across a wide array of forecasting tasks and outperformed traditional methods as well as other deep learning models in numerous benchmarks.",
    advantages=[
        "High accuracy: N-BEATS consistently achieves superior performance compared to traditional methods and other deep learning models.",
        "Interpretability: The model's ability to learn interpretable components offers valuable insights into the underlying structure of time series data.",
        "Flexibility: N-BEATS can adapt to a wide range of time series patterns, making it suitable for diverse forecasting tasks.",
        "Scalability: The model can be easily scaled to handle large datasets or high-dimensional input features.",
    ],
    disadvantages=[
        "Requires large amounts of training data: N-BEATS requires a large amount of training data to learn the underlying patterns in the data."
        "Computational complexity: N-BEATS may require considerable computational resources for training, especially for large datasets or complex models.",
        "Risk of overfitting: Like any deep learning model, N-BEATS can overfit the training data, which may result in reduced performance on unseen data.",
        "Limited interpretability compared to some traditional methods: Although N-BEATS offers some level of interpretability, it may not be as transparent as simpler models like ARIMA or exponential smoothing.",
        "Dependency on quality of input data: The model's performance depends heavily on the quality and relevance of the input features used for training.",
    ],
    prime=[],
    display_name="N-BEATS Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
