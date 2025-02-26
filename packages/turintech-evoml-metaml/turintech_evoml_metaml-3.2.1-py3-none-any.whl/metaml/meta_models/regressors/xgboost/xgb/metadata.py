from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.xgboost_regressor,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.regressor, ModelTag.custom_io},
    description="The XGBoost Regressor is a powerful and efficient gradient boosting model from the XGBoost library. It combines multiple weak learners, typically decision trees, to create a strong ensemble model. In each iteration, a new weak learner is added to the ensemble, focusing on correcting the errors made by the previous learners. Predictions from the ensemble model are given by a weighted sum of the predictions of the individual weak learners. XGBoost Regressor is known for its high performance, scalability, and ability to handle various data types and distributions, making it a popular choice for a wide range of machine learning tasks, especially regression problems.",
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
    display_name="XGBoost Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
