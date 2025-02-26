from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.lightgbm_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier},
    description="LightGBM Classifier is a tree-based ensemble model. It buckets continuous feature values into discrete bins and uses a gradient-based one-side sampling to split values. In comparison with XGBoost and CatBoost, LightGBM performs poorly on categorical datasets but has a similar performance to XGBoost on numerical datasets with fewer training time.",
    advantages=[
        "It is computational efficient",
        "It performs well on large sized datasets",
    ],
    disadvantages=["It has the problem of overfitting especially on small data"],
    prime=[],
    display_name="LightGBM Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
