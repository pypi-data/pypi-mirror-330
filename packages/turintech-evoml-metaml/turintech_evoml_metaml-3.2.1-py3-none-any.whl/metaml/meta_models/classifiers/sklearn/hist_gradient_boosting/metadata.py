from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.hist_gradient_boosting_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier, ModelTag.experimental},
    description="Histogram-based Gradient Boosting Classifier is much faster than the Gradient Boosting Classifier for big datasets (n_samples >= 10 000). It has native support for missing values (NaNs). During training, the tree grower learns at each split point whether samples with missing values should go to the left or right child, based on the potential gain. When predicting, samples with missing values are assigned to the left or right child consequently.",
    advantages=["It requires no pre-processing of data like the normalization and the scaling of data"],
    disadvantages=[
        "It is sensitive to outliers",
        "It has the problem of overfitting",
        "It is computationally expensive",
    ],
    prime=[],
    display_name="Histogram-based Gradient Boosting Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
