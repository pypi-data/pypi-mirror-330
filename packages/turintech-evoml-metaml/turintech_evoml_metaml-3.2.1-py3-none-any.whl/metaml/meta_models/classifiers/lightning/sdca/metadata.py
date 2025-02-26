from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.sdca_classifier,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.classifier},
    description="The Stochastic Dual Coordinate Ascent (SDCA) Classifier is a linear classification model that utilizes the SDCA optimization algorithm. It is designed for large-scale learning scenarios and is efficient for high-dimensional sparse data.",
    advantages=[
        "Efficient on large datasets due to its incremental nature.",
        "Converges quickly for sparse data.",
        "Less sensitive to the choice of hyperparameters compared to some other optimization algorithms.",
        "Good for high-dimensional data.",
    ],
    disadvantages=[
        "Primarily suited for linear classification, limiting its applicability for complex, non-linear problems.",
        "The quality of the solution may depend on the initial conditions.",
        "Does not directly support probability estimates.",
        "May require careful feature scaling.",
    ],
    prime=[],
    display_name="Stochastic Dual Coordinate Ascent Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
