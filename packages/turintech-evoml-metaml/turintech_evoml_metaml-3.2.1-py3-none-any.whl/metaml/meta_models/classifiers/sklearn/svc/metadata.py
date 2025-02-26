from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.svm_classifier,
    model_type={ModelTypeEnum.support_vector_machine, ModelTypeEnum.kernel},
    tags={ModelTag.classifier},
    description="Support Vector Machine Classifier builds a hyperplane with support vectors to separate marked example points.",
    advantages=[
        "It performs well in higher dimension spaces",
        "It is robust to outliers",
        "It is memory efficient",
    ],
    disadvantages=[
        "It is computationally expensive",
        "It is tricky in selecting the appropriate kernel function",
    ],
    prime=[],
    display_name="Support Vector Machine Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
