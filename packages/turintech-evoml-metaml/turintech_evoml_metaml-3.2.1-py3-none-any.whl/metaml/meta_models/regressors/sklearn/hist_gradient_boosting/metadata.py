from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.hist_gradient_boosting_regressor,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.regressor, ModelTag.experimental},
    description="Histogram-based Gradient Boosting Regressor is much faster than the Gradient Boosting Regressor for big datasets (n_samples >= 10 000). It has native support for missing values (NaNs). During training, the tree grower learns at each split point whether samples with missing values should go to the left or right child, based on the potential gain. When predicting, samples with missing values are assigned to the left or right child consequently.",
    advantages=["It requires no pre-processing of data like the normalization and the scaling of data"],
    disadvantages=[
        "It is sensitive to outliers",
        "It has the problem of overfitting",
        "It is computationally expensive",
    ],
    prime=[],
    display_name="Histogram-based Gradient Boosting Regressor",
    supports=Supports(probabilities=False, feature_importances=False),
)
