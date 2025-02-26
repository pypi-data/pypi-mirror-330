from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.cd_classifier,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.classifier},
    description="The Coordinate Descent Classifier is a machine learning algorithm designed to optimize linear classifiers through (block) coordinate descent methods. It is particularly useful for large-scale and sparse data sets.",
    advantages=[
        "Scalable to large data sets.",
        "Efficient handling of sparse data.",
        "Fine-grained control through various hyperparameters.",
    ],
    disadvantages=[
        "May be sensitive to feature scaling.",
        "Limited to linear decision boundaries.",
        "Requires careful tuning of hyperparameters.",
    ],
    prime=[],
    display_name="Coordinate Descent Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
