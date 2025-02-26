from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.fista_regressor,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.regressor},
    description="An estimator that employs the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA) for training linear regression models. Designed for rapid convergence, FISTA is particularly advantageous for tackling large-scale and high-dimensional problems. The algorithm promotes sparse solutions, making it memory-efficient. It is well-suited for convex optimization tasks and offers flexibility in terms of regularization techniques.",
    advantages=[
        "Rapid Convergence: FISTA is designed for fast convergence, making it highly suitable for large and high-dimensional datasets.",
        "Promotes Sparse Solutions: The algorithm encourages sparsity in the feature coefficients, which is advantageous in high-dimensional scenarios where feature selection is essential.",
        "Memory-Efficient: Unlike some other optimization algorithms, FISTA does not require the storage of large intermediate matrices, making it resource-efficient.",
    ],
    disadvantages=[
        "Hyperparameter Sensitivity: The performance of the FISTA Regressor can be sensitive to the choice of hyperparameters, requiring careful tuning for optimal results.",
        "Numerical Instabilities: Similar to its classifier counterpart, the FISTA Regressor may suffer from numerical instabilities, which could impact its performance and reliability.",
    ],
    prime=[],
    display_name="Fast Iterative Shrinkage/Thresholding Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
