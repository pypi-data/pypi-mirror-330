from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.lightgbm_regressor,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.regressor},
    description="The LightGBM Regressor is a gradient boosting framework based on decision trees from the LightGBM library. It uses a novel technique called Gradient-based One-Side Sampling (GOSS) to filter out the data instances for finding a split value, and Exclusive Feature Bundling (EFB) to reduce the number of features during training. This results in a faster training process and lower memory usage while maintaining high accuracy.",
    advantages=[
        "Faster training speed and lower memory usage compared to other gradient boosting frameworks.",
        "High accuracy and good generalization performance.",
        "Supports parallel and GPU learning.",
        "Handles large-scale data and high-dimensional features well.",
    ],
    disadvantages=[
        "Requires careful tuning of hyperparameters for optimal performance.",
        "Less interpretable than simpler models like linear regression.",
        "Not as robust to noise and outliers as some other models.",
    ],
    prime=[],
    display_name="LightGBM Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
