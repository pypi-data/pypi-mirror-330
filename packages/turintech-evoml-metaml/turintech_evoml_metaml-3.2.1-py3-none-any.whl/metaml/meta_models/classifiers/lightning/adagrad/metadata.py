from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.adagrad_classifier,
    model_type={ModelTypeEnum.gradient},
    tags={ModelTag.classifier},
    description="This estimator is designed to leverage the AdaGrad (Adaptive Gradient Algorithm) optimization technique for training linear classifiers. The model dynamically adjusts the learning rate for each feature during training, which makes it well-suited for datasets that are sparse or high-dimensional. It is designed to minimize convex loss functions and generally requires less hyperparameter tuning compared to some other optimization algorithms.",
    advantages=[
        "Adaptive Learning Rate for Each Feature: One of the primary benefits of using this model is its adaptive learning rate, which adjusts individually for each feature. This characteristic is particularly advantageous when dealing with sparse or imbalanced data, as it allows the model to focus more on the important features.",
        "Easier Hyperparameter Tuning: The adaptive learning rates mean that the model is generally less sensitive to the initial choice of learning rate, which makes the task of hyperparameter tuning simpler and potentially faster.",
        "Effective for Convex Problems: The AdaGrad algorithm is efficient at finding the global minimum when the problem is convex. This makes it suitable for a wide range of machine learning problems where the loss function is convex.",
    ],
    disadvantages=[
        "Learning Rate Decay Issues: One of the drawbacks of the AdaGrad algorithm is that the learning rate for each feature can decrease to a point where the model makes very little progress. This is especially problematic for non-convex problems, where it can prevent the model from reaching the global minimum.",
        "Memory Overheads: The model tracks the sum of squares of past gradients for each feature, which increases its memory consumption. This may not be ideal for systems with limited memory resources.",
        "Computation Overheads: Although the model adjusts the learning rate for each feature, this operation can be computationally expensive, particularly for high-dimensional data sets. This could be a bottleneck in terms of both speed and computational resources when working with large, high-dimensional data.",
    ],
    prime=[],
    display_name="Adaptive Gradient Classifier",
    supports=Supports(probabilities=False, feature_importances=True),
)
