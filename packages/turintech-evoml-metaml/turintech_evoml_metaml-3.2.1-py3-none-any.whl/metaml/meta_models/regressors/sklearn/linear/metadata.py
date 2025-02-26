from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.linear_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description="The Linear Regressor is a fundamental statistical model that aims to establish a linear relationship between a set of input features and a continuous output variable. It is simple, interpretable, and computationally efficient, making it a good baseline model for many predictive tasks. The method seeks to fit a linear equation to observed data by minimizing the sum of the squared differences between the observed outcomes and the outcomes predicted by the model.",
    advantages=[
        "Interpretability: One of the main advantages of Linear Regression is its high interpretability. The coefficients of the model directly indicate the impact of each feature on the target variable, making it easy to explain the model's decisions.",
        "Low Computational Cost: Linear Regression is computationally inexpensive to train and predict, making it highly scalable for datasets with a large number of samples and features.",
        "Fast to Implement and Train: Due to its simplicity and the availability of analytical solutions, a Linear Regressor can be quickly implemented and trained, serving as a useful baseline model in many machine learning projects.",
    ],
    disadvantages=[
        "Prone to Overfitting with High-Dimensional Data: In cases where the number of features is greater than the number of observations, or when features are highly correlated, Linear Regression is susceptible to overfitting.",
        "Assumes Linear Relationship: Linear Regression assumes that the relationship between the features and the target variable is linear. This assumption may not hold for complex, real-world data sets where relationships can be non-linear.",
        "Sensitive to Outliers: The model is sensitive to outliers in the data, which can disproportionately affect the slope of the regression line and, consequently, the predictions.",
    ],
    prime=[],
    display_name="Linear Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
