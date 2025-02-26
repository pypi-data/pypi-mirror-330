from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.linearsvc_classifier,
    model_type={ModelTypeEnum.support_vector_machine, ModelTypeEnum.kernel},
    tags={ModelTag.classifier},
    description="Linear Support Vector Machine Classifier is similar to Support Vector Machine Classifier with the linear kernel but has more flexibility in the choice of penalties and loss functions.",
    advantages=[
        "It performs well in higher dimension spaces",
        "It is robust to outliers",
    ],
    disadvantages=[
        "It is computationally expensive",
        "It is tricky in selecting the appropriate kernel function",
    ],
    prime=[],
    display_name="Linear Support Vector Machine Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
