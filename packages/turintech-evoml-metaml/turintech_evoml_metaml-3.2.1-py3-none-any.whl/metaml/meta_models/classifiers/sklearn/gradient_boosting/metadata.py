from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.gradient_boosting_classifier,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.classifier},
    description="Gradient Boosting Classifier builds an additive model in a forward stage-wise fashion; it allows for the optimization of arbitrary differentiable loss functions. In each stage, n_classes_ classifier trees are fitted on the negative gradient of the binomial or multinomial deviance loss function.",
    advantages=["It requires no pre-processing of data like the normalization and the scaling of data"],
    disadvantages=[
        "It is sensitive to outliers",
        "It has the problem of overfitting",
        "It is computationally expensive",
    ],
    prime=[],
    display_name="Gradient Boosting Classifier",
    supports=Supports(probabilities=True, feature_importances=True),
)
