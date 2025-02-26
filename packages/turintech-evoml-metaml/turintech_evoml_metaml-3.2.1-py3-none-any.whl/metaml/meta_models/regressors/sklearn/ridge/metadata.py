from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.ridge_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description="The Ridge Regressor is a type of linear regression model that incorporates L2 regularization to penalize large coefficients in the predictive variables. By adding a squared magnitude term of the coefficients in the loss function, Ridge regression discourages overly complex models, thereby reducing overfitting. It is particularly useful in scenarios where the number of features is large compared to the number of observations or when features are correlated, which can lead to multicollinearity issues in standard linear regression.",
    advantages=[
        "Prevention of Overfitting: Ridge Regression helps prevent overfitting by adding a penalty term to the loss function, encouraging the model to keep the weight of each feature as small as possible. This makes it more robust when faced with irrelevant or highly correlated features.",
        "Stable Solutions in High-Dimensional Space: Ridge Regression performs well even when the number of features is greater than the number of observations, providing a stable solution where ordinary least squares would fail.",
        "Handles Multicollinearity: Ridge Regression deals effectively with multicollinearity (correlation between predictor variables) by distributing the coefficients among them. This makes it useful in applications where features are correlated, as it provides a more stable and robust estimate.",
    ],
    disadvantages=[
        "No Feature Selection: Unlike methods such as Lasso or Elastic Net, Ridge Regression does not set any coefficients to zero, making all features part of the final model. This can make the model less interpretable when there are many irrelevant features.",
        "Requires Hyperparameter Tuning: The strength of the regularization is controlled by a hyperparameter that needs to be tuned, adding to the complexity and computational cost of model development.",
        "Sensitive to Feature Scaling: Just like Elastic Net, Ridge Regression is sensitive to the scale of input features. Therefore, feature scaling is often necessary as a preprocessing step to ensure that all features are treated equally by the regularization term.",
    ],
    prime=[],
    display_name="Ridge Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
