from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.passive_aggressive_classifier,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.classifier},
    description="Passive Aggressive Classifier is a family of algorithms for large-scale learning. It is similar to the Perceptron in that they do not require a learning rate but contrary to the Perceptron in that they include a regularization parameter.",
    advantages=["It is suitable for large-scale learning"],
    disadvantages=["It has the problem of learning many simple functions"],
    prime=[],
    display_name="Passive Aggressive Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
