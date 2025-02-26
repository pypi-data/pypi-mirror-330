from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.nearest_centroid_classifier,
    model_type={ModelTypeEnum.nearest_neighbours},
    tags={ModelTag.classifier},
    description="Nearest Centroid Classifier is a specialized type of neighbor classifier model which represents each class by the centroid of its members.",
    advantages=[
        "It is easy to understand and implement",
        "It works well when classes are compact and far from each other",
    ],
    disadvantages=[
        "It has poor performance for complex classes",
        "It can not handle outliers noisy data and missing data well",
    ],
    prime=[],
    display_name="Nearest Centroid Classifier",
    supports=Supports(probabilities=False, feature_importances=False),
)
