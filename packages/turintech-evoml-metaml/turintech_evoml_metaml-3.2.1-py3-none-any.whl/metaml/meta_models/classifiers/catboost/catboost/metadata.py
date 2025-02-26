from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.catboost_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier},
    description="The CatBoost Classifier is a gradient-boosting model specialized in handling categorical features through permutation-driven techniques. It uses ordered boosting to reduce overfitting and symmetric trees for faster execution. It is often compared favorably to XGBoost and LightGBM, particularly when dealing with categorical data.",
    advantages=[
        "Handles categorical features well",
        "Reduced overfitting through ordered boosting",
        "Fast execution with symmetric trees",
        "Competitive performance compared to XGBoost and LightGBM",
        "Robust default settings",
    ],
    disadvantages=[
        "Higher memory consumption",
        "Less interpretable than simpler models",
        "May require parameter tuning for optimal performance",
        "Can be slower to train on very large datasets",
    ],
    prime=[],
    display_name="CatBoost Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
