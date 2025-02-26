from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.random_forest_regressor,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.regressor},
    description="The Random Forest Regressor is a versatile and powerful ensemble learning method from the scikit-learn library. It works by constructing multiple decision trees during training and outputting the mean prediction of the individual trees. This model is particularly effective for handling large datasets with high dimensionality and can automatically learn feature interactions.",
    advantages=[
        "Effective for large datasets and high-dimensional features",
        "Automatically learns feature interactions",
        "Reduces overfitting compared to single decision trees",
        "Provides feature importance scores",
        "Can handle missing data and requires minimal data preprocessing",
    ],
    disadvantages=[
        "Can be computationally expensive due to the large number of trees",
        "Less interpretable than single decision trees",
        "Slower prediction time compared to some other models",
        "May not perform well on very small datasets or with very noisy data",
    ],
    prime=[],
    display_name="Random Forest Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
