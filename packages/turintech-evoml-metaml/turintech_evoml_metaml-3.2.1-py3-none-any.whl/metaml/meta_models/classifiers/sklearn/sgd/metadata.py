from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.sgd_classifier,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.classifier},
    description="Stochastic Gradient Descent Classifier is a linear classifier with stochastic gradient descent (SGD) training. The gradient of the loss is estimated each sample at a time and the model is updated along the way with a decreasing strength schedule.",
    advantages=[
        "It is computationally efficient",
        "It has fast convergence for larger datasets",
    ],
    disadvantages=["It is not stable"],
    prime=[],
    display_name="Stochastic Gradient Descent Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
