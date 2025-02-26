from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.lasso_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description="The Lasso Regressor is a linear regression model that employs L1 regularization to add a penalty term to the loss function, which is proportional to the absolute value of the coefficients. This form of regularization encourages sparsity by forcing some coefficients to be exactly zero, effectively performing feature selection. Lasso is particularly useful when you suspect that many features are irrelevant or redundant, and you want a model that is easier to interpret.",
    advantages=[
        "Feature Selection: One of the key advantages of Lasso Regression is its ability to perform automatic feature selection. By forcing some coefficient estimates to be exactly zero, it provides a model that involves only a subset of the features, making the model easier to interpret and generalize.",
        "Prevention of Overfitting: Similar to Ridge and Elastic Net, Lasso also adds a penalty term to the loss function, discouraging overly complex models and thus helping to prevent overfitting.",
        "Works Well with High-Dimensional Data: Lasso Regression can provide good performance even when the number of features is greater than the number of samples, especially when only a subset of the features is relevant for prediction.",
    ],
    disadvantages=[
        "Stability Issues: Lasso can be unstable in cases where predictors are highly correlated. In such cases, it may arbitrarily choose one feature over another, which may vary with slight changes in the data.",
        "Hyperparameter Tuning: Just like Ridge and Elastic Net, Lasso also requires the tuning of a regularization strength hyperparameter, which can add to the complexity and computational time needed for model development.",
        "Limitation in Model Complexity: By zeroing out some of the coefficients, Lasso may produce a model that is too simplistic to capture the underlying patterns in the data, especially if the true relationship requires inclusion of all features.",
    ],
    prime=[],
    display_name="Lasso Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
