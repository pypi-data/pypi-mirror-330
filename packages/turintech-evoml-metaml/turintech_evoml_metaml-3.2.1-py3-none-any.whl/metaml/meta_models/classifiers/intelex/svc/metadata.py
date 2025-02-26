from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.intelex_svm_classifier,
    model_type={ModelTypeEnum.support_vector_machine, ModelTypeEnum.kernel},
    tags={ModelTag.classifier},
    description="Support Vector Machine Classifier builds a hyperplane with support vectors to separate marked example points.",
    advantages=[
        "Support Vector Machines (SVMs) perform well in high-dimensional spaces, making them suitable for datasets with many features.",
        "They use a subset of training points in the decision function (support vectors), making them memory efficient.",
        "They're versatile, as different Kernel functions can be specified for the decision function.",
    ],
    disadvantages=[
        "They are not efficient with large datasets because the training time can be cubic in the size of the dataset.",
        "SVMs don't provide probability estimates directly, which can be a disadvantage in certain use cases.",
        "If the number of features greatly exceeds the number of samples, the SVM can perform poorly and overfitting can occur.",
    ],
    prime=[],
    display_name="Intelex Support Vector Machine Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
