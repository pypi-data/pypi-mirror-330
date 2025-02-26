from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.logistic_regression_classifier,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.classifier},
    description="The logistic regression classifier is a linear model for classification, implemented in the scikit-learn library. It estimates the probability of an instance belonging to a specific class by fitting a logistic function to the input data. The model supports various regularization techniques, solvers, and multi-class strategies.",
    advantages=[
        "Ease of implementation and effectiveness",
        "Computational efficiency",
        "Low likelihood of overfitting",
    ],
    disadvantages=[
        "Struggles with non-linear data",
        "Impaired performance due to irrelevant or highly correlated features",
    ],
    prime=[],
    display_name="Logistic Regression Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
