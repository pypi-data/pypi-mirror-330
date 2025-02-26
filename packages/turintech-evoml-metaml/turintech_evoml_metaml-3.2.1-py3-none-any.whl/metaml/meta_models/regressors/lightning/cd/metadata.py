from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.cd_regressor,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.regressor},
    description="The Coordinate Descent Regressor is a machine learning algorithm designed to optimize linear regression models through (block) coordinate descent methods. It is particularly well-suited for large-scale and sparse datasets.",
    advantages=[
        "Scalable to Large Datasets: The algorithm is designed to efficiently handle large volumes of data, making it suitable for applications with massive datasets.",
        "Efficient Handling of Sparse Data: The Coordinate Descent Regressor can effectively manage sparse datasets, optimizing computational resources and potentially improving model performance.",
        "Fine-Grained Control: The model offers various hyperparameters that provide fine-grained control over the optimization process, allowing for customized model tuning.",
    ],
    disadvantages=[
        "Sensitive to Feature Scaling: Similar to its classifier counterpart, the Coordinate Descent Regressor may also be sensitive to the scaling of features, requiring pre-processing steps.",
        "Limited to Linear Relationships: The model is primarily designed for linear regression tasks, making it less suitable for capturing complex, non-linear relationships in the data.",
        "Hyperparameter Tuning Required: The performance of the model may be highly dependent on the appropriate tuning of hyperparameters, adding to the complexity and time required for model development.",
    ],
    prime=[],
    display_name="Coordinate Descent Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
