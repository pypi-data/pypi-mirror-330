from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.gaussian_process_classifier,
    model_type={ModelTypeEnum.bayesian, ModelTypeEnum.kernel},
    tags={ModelTag.classifier},
    description="Gaussian Process Classifier is a nonparametric, bayesian probabilistic classification using a Gaussian process as a prior over random functions and Laplace approximation as the non-Gaussian posterior.",
    advantages=[
        "It performs well on small datasets",
        "It has the ability to provide uncertainty measurements on the predictions",
        "It has the flexibility in using different kernels",
    ],
    disadvantages=["It loses efficiency in high dimensional spaces"],
    prime=[],
    display_name="Gaussian Process Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
