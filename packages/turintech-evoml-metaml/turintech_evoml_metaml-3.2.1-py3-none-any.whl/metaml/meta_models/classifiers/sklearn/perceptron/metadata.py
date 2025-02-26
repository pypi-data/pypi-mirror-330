from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.perceptron_classifier,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.classifier},
    description="The Perceptron Classifier is a linear classification model based on a simple artificial neural unit. It iteratively adjusts weights in the input features to find a hyperplane that separates two classes. It is well-suited for high-dimensional data and is one of the simplest types of classifiers.",
    advantages=[
        "Simple and easy to understand",
        "Fast to train",
        "Works well with high-dimensional data",
        "Low computational requirements",
    ],
    disadvantages=[
        "Sensitive to feature scaling",
        "Not suitable for non-linearly separable data",
        "May not converge if data is not linearly separable",
        "Lacks probabilistic interpretation",
    ],
    prime=[],
    display_name="Perceptron Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
