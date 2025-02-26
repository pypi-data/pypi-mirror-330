from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.extra_trees_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier},
    description="The Extremely Randomized Trees (Extra-Trees) Classifier is an ensemble model that builds multiple randomized decision trees and averages their predictions. This approach aims to improve accuracy and reduce overfitting.",
    advantages=[
        "Robust to overfitting",
        "Highly parallelizable",
        "Provides feature importance",
        "Quick to train",
        "Versatile",
    ],
    disadvantages=[
        "Low interpretability",
        "High memory usage",
        "Predictive variability",
        "Less accurate than some boosting methods",
        "Requires hyperparameter tuning",
    ],
    prime=[],
    display_name="Extremely Randomized Tree Ensemble Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
