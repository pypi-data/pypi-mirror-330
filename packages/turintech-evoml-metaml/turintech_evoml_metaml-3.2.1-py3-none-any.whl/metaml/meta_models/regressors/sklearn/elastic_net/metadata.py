from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.elastic_net_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description="The Elastic Net Regressor is a linear regression model that combines the strengths of both Lasso and Ridge regression techniques. By incorporating both L1 and L2 regularization terms, it provides a balanced approach to penalize coefficients, enabling the model to prevent overfitting while dealing effectively with correlated features. It is particularly useful when there are many correlated variables in the dataset, as it tends to distribute feature importance relatively equally among correlated variables while also performing feature selection.",
    advantages=[
        "Versatility in Handling Correlated Features: Elastic Net can effectively manage correlated features by blending L1 and L2 regularizations. This provides a balanced approach that tends to distribute the weight of importance among correlated variables.",
        "Prevents Overfitting While Enabling Feature Selection: Unlike Ridge regression, which can't set coefficients to zero, or Lasso, which can be inconsistent in high-dimensional spaces, Elastic Net brings the best of both worlds. It helps to prevent overfitting and, at the same time, can shrink less important features' coefficients to zero, performing automatic feature selection.",
        "Stability and Uniqueness: Elastic Net provides model stability under conditions where Lasso would produce multiple solutions due to highly correlated predictors. The Ridge component of Elastic Net ensures that a unique solution exists, which aids in model interpretability and consistency.",
    ],
    disadvantages=[
        "Computational Complexity: Elastic Net requires the tuning of two hyperparameters, which increases computational time and complexity. This can make grid search or other hyperparameter tuning methods more time-consuming compared to simpler models.",
        "Reduced Interpretability: While still more interpretable than many non-linear models, the inclusion of both L1 and L2 regularizations makes Elastic Net somewhat harder to interpret than standard Linear Regression.",
        "Sensitivity to Scaling: Elastic Net is sensitive to the scale of input features. Feature scaling is usually required to ensure that the regularization treats all features equally, adding an extra preprocessing step.",
    ],
    prime=[],
    display_name="Elastic Net Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
