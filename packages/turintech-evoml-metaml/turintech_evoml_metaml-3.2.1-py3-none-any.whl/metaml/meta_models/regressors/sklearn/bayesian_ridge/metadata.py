from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.bayesian_ridge_regressor,
    model_type={ModelTypeEnum.linear, ModelTypeEnum.bayesian},
    tags={ModelTag.regressor},
    description="Bayesian Ridge Regressor is a specialized type of Bayesian regression and uses a spherical Gaussian prior to fit the weights, which is also similar to the classical Ridge model.",
    advantages=[
        "It adapts to the data at hand",
        "It can be used to include regularization parameters in the estimation procedure",
    ],
    disadvantages=["Inference of the model can be time consuming"],
    prime=[],
    display_name="Bayesian Ridge Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
