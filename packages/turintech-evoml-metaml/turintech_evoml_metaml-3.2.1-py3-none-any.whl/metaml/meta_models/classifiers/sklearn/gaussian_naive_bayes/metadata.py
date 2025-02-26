from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.gaussian_naivebayes_classifier,
    model_type={ModelTypeEnum.bayesian},
    tags={ModelTag.classifier},
    description="Gaussian Naive Bayes Classifier implements the Gaussian Naive Bayes training and classification algorithm for classification. The likelihood of the features is assumed to be Gaussian. It can perform online updates to model parameters via partial_fit.",
    advantages=[
        "It is computational efficient",
        "It performs well on small amounts of data",
        "It can handle irrelevant features nicely",
    ],
    disadvantages=[
        "It has a strong assumption based on the shape of data",
        "It is not stable",
    ],
    prime=[],
    display_name="Gaussian Naive Bayes Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
