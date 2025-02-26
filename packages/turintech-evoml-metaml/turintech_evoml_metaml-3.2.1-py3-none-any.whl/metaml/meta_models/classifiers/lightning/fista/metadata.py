from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.fista_classifier,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.classifier},
    description="An estimator that employs the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA) for training linear classifiers. Designed for fast convergence, FISTA is particularly well-suited for large-scale and high-dimensional problems. It encourages sparse solutions and is efficient in terms of memory usage. The algorithm is ideal for convex optimization problems and offers flexibility in regularization techniques.",
    advantages=[
        "Fast convergence, especially suitable for large datasets.",
        "Encourages sparse solutions, advantageous in high-dimensional settings.",
        "Resource-efficient, doesn't require storing large intermediate matrices.",
    ],
    disadvantages=[
        "Sensitive to the choice of hyperparameters, requiring careful tuning.",
        "May suffer from numerical instabilities.",
    ],
    prime=[],
    display_name="Fast Iterative Shrinkage/Thresholding Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
