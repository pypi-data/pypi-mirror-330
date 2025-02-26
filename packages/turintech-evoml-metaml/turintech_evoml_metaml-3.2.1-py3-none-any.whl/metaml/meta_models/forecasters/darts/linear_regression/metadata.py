from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ForecasterName


metadata = MetaData(
    model_name=ForecasterName.linear_regression_forecaster,
    model_type={ModelTypeEnum.baseline},
    tags={ModelTag.ts, ModelTag.forecaster},
    description="The Linear Regression forecaster from the darts library is a statistical method used to predict a dependent variable (target) based on the values of independent variables (features). The model assumes a linear relationship between the input variables and the output. The model's strength lies in its simplicity and interpretability. It can be used to understand the impact of several independent variables on the outcome of a dependent variable. Linear Regression is widely used in various fields, including economics, computer science, and the social sciences.",
    advantages=[
        "Simplicity: Linear Regression is straightforward to understand and explain, making it a good model for beginners.",
        "Interpretability: Each feature used in the model gets its own coefficient which tells its importance in the prediction.",
        "Speed: Linear Regression is computationally inexpensive compared to more complex models and hence, is useful for large datasets.",
    ],
    disadvantages=[
        "Assumptions: Linear Regression assumes a linear relationship between features and target variable, which is not always the case.",
        "Outliers: The model is sensitive to outliers which can have a large influence on the line of best fit.",
        "Overfitting: With many features, the model can become complex and may overfit the training data, resulting in poor performance on unseen data.",
    ],
    prime=[],
    display_name="Linear Regression Forecaster",
    supports=Supports(probabilities=False, feature_importances=False),
)
