from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.ard_regressor,
    model_type={ModelTypeEnum.linear, ModelTypeEnum.bayesian},
    tags={ModelTag.regressor},
    description="The Automatic Relevance Determination (ARD) model is a Bayesian linear regression model from the scikit-learn library that extends the traditional linear regression model by incorporating priors on the model parameters. It aims to estimate the relevance of each input feature by learning individual regularization parameters for each feature. This results in a form of automatic feature selection, as irrelevant or redundant features are assigned larger regularization parameters, effectively reducing their impact on the model's predictions. The ARD model uses an iterative optimization process to estimate both the model parameters and the hyperparameters associated with the priors. This Bayesian approach allows the model to quantify the uncertainty in its predictions, providing a measure of confidence alongside the predicted values. The ARD model is particularly useful for regression tasks with high-dimensional data, where the underlying structure of the data is unknown, and automatic feature selection or sparsity is desired.",
    advantages=[
        "Automatically selects regularization parameters.",
        "Identifies the most relevant features for the regression task.",
        "Can handle multicollinearity in the input features.",
        "Reduces model complexity by pruning less important features.",
    ],
    disadvantages=[
        "Sensitive to the choice of hyperparameters.",
        "May require more iterations to converge compared to other linear regression models.",
        "Not suitable for very large datasets due to computational complexity.",
    ],
    prime=[],
    display_name="Automatic Relevance Determination Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
