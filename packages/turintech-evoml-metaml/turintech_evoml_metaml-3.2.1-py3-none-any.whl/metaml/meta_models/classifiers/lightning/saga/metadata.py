from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.saga_classifier,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.classifier},
    description="Stochastic Average Gradient (SAGA) is an optimization algorithm frequently employed for large-scale machine learning tasks. It is especially useful for handling high-dimensional data and large datasets. SAGA is an extension of Stochastic Gradient Descent (SGD) and aims to merge the benefits of batch and stochastic optimization methods. While it is commonly used for linear classifiers like logistic regression, it can also be adapted for other types of models.",
    advantages=[
        "Scalability: SAGA is engineered to efficiently handle large datasets and scales well with the number of observations.",
        "Memory Efficiency: Unlike full-batch methods, SAGA allows for the optimization of the model without needing to store the entire dataset in memory, which is more memory-efficient.",
        "Fast Convergence: For convex optimization problems, SAGA generally converges faster than traditional batch methods or standard stochastic methods.",
        "Robustness: SAGA is less sensitive to initial learning rate settings and other hyperparameters compared to standard SGD.",
        "Parallelism: While the core algorithm is inherently sequential, some level of parallelism can be achieved through data distribution.",
    ],
    disadvantages=[
        "Non-Convexity: SAGA is primarily designed for convex optimization problems, and its performance may suffer when applied to non-convex problems.",
        "Tuning Required: Despite being less sensitive to hyperparameters than other optimization methods, some tuning is often still required for optimal performance.",
        "Warm Start Sensitivity: The algorithm's performance may vary depending on the initial conditions, particularly when a warm start is utilized.",
        "Stochastic Nature: While this is less of an issue for convex problems, the stochastic nature of the algorithm means that it may oscillate around the global minimum for non-convex problems.",
        "Implementation Complexity: SAGA is more challenging to implement than simpler optimization algorithms like batch gradient descent.",
    ],
    prime=[],
    display_name="Stochastic Averaged Gradient Ascent Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
