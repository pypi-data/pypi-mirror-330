from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.svr_regressor,
    model_type={ModelTypeEnum.support_vector_machine, ModelTypeEnum.kernel},
    tags={ModelTag.regressor, ModelTag.experimental},
    description="The SVR Regressor is a Support Vector Regression model from the scikit-learn library. It is an extension of the Support Vector Machine (SVM) algorithm for regression tasks. The model aims to find a function that approximates the relationship between input features and target values with a specified tolerance (epsilon). It uses different kernel functions to transform the input data into a higher-dimensional space, where a linear function is fitted to minimize the error between predicted and actual target values.",
    advantages=[
        "Effective in high-dimensional spaces.",
        "Supports different kernel functions for versatile modeling.",
        "Robust against overfitting, especially when using a high-dimensional feature space.",
    ],
    disadvantages=[
        "Can be slow to train on large datasets.",
        "Requires careful selection of kernel and hyperparameters.",
    ],
    prime=[],
    display_name="SVR Regressor",
    supports=Supports(probabilities=False, feature_importances=False),
)
