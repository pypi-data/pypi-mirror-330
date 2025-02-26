from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.intelex_random_forest_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier},
    description="Random Forest Classifier is a specialized type of tree-based model implementing meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.",
    advantages=[
        "It performs well on imbalanced datasets",
        "It is robust to outliers",
        "There is more generalization and less overfitting",
        "It is useful to extract feature importance",
    ],
    disadvantages=["It requires that features need to have some predictive power"],
    prime=[],
    display_name="Intelex Random Forest Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
