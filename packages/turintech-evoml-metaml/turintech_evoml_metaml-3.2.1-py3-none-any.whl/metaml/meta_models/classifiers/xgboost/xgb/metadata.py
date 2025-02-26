from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.xgboost_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier, ModelTag.custom_io},
    description="The XGBoost Classifier is a powerful and efficient gradient boosting model from the XGBoost library. It combines multiple weak learners, typically decision trees, to create a strong ensemble model. In each iteration, a new weak learner is added to the ensemble, focusing on correcting the errors made by the previous learners. Predictions from the ensemble model are given by a weighted sum of the predictions of the individual weak learners. XGBoost Classifier is known for its high performance, scalability, and ability to handle imbalanced datasets, making it a popular choice for a wide range of machine learning tasks.",
    advantages=[
        "It requires less feature engineering",
        "Feature importance can be found out",
        "It is robust to outliers",
        "It performs well on large sized datasets",
        "It is computational fast",
    ],
    disadvantages=[
        "It has the problem of overfitting",
        "It is harder to tune as there are too many hyperparameters",
    ],
    prime=[],
    display_name="XGBoost Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
