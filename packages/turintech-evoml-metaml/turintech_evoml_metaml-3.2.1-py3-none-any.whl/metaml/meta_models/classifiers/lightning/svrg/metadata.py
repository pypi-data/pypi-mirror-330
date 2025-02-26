from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.svrg_classifier,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.classifier},
    description="The Stochastic Variance-reduced Gradient (SVRG) Classifier is designed for large-scale optimization and is particularly well-suited for problems with a lot of features.",
    advantages=[
        "Efficient for high-dimensional data.",
        "Reduces variance in the stochastic gradients, accelerating convergence.",
        "Well-suited for sparse data.",
        "Performs well in large-scale optimization scenarios.",
    ],
    disadvantages=[
        "Can be sensitive to hyperparameters like step size.",
        "Not as versatile for non-linear problems as some other methods.",
        "Requires more computational resources for maintaining and updating gradients.",
    ],
    prime=[],
    display_name="Stochastic Variance-reduced Gradient Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
