from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.quadratic_discriminant_analysis_classifier,
    model_type={ModelTypeEnum.bayesian},
    tags={ModelTag.classifier},
    description="Quadratic Discriminant Analysis Classifier generates a quadratic decision boundary via fitting class conditional densities to the data and applying Bayes rule. In this model, all classes are assumed to share the same covariance matrix and fitted by the Gaussian density.",
    advantages=[
        "It has a closed-form solution",
        "It is easy to implement",
        "It has no hyperparameters to tune",
    ],
    disadvantages=["It requires normal distribution assumption on features"],
    prime=[],
    display_name="Quadratic Discriminant Analysis Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
