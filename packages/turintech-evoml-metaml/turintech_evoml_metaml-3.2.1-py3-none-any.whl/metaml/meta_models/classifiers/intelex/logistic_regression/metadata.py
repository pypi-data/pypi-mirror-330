from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.intelex_logistic_regression_classifier,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.classifier},
    description="The logistic regression classifier is a linear model for classification, implemented using the scikit-learn library. It estimates the probability of an instance belonging to a specific class by fitting a logistic function to the input data. The model supports various regularization techniques, solvers, and multi-class strategies.",
    advantages=[
        "Logistic regression provides probabilities of each class label, which helps the user judge the confidence of predictions",
        "It is simple to understand and explain, which supports interpretability.",
        "It handles binary and multiclass classification problems, enhancing its applicability.",
    ],
    disadvantages=[
        "Logistic regression assumes linearity of independent variables and log odds, limiting its use in complex nonlinear relationships.",
        "It might be prone to overfitting, particularly in scenarios with many input features.",
        "It's not ideal for large number of features or variables, due to the risk of multicollinearity.",
    ],
    prime=[],
    display_name="Intelex Logistic Regression Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
