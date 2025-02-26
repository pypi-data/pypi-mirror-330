from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.sgd_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description="Stochastic Gradient Descent Regressor is a linear regression model with stochastic gradient descent (SGD) training. The gradient of the loss is estimated each sample at a time and the model is updated along the way with a decreasing strength schedule.",
    advantages=[
        "It is computationally efficient",
        "It has fast convergence for larger datasets",
    ],
    disadvantages=["It is not stable"],
    prime=[],
    display_name="Stochastic Gradient Descent Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
