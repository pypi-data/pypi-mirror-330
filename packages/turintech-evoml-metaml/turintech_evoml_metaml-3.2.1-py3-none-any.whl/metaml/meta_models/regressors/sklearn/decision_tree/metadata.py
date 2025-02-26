from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.decision_tree_regressor,
    model_type={ModelTypeEnum.tree},
    tags={ModelTag.regressor},
    description="Decision Trees Regressor predicts the value of a target variable by learning simple decision rules inferred from the data features.",
    advantages=[
        "It requires no pre-processing of data like the normalization and the scaling of data  Missing values in the data also do not affect"
    ],
    disadvantages=[
        "A small change in the data can cause a large change",
        "It is computational expensive",
    ],
    prime=[],
    display_name="Decision Tree Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
