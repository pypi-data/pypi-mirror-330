from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.passive_aggressive_regressor,
    model_type={ModelTypeEnum.linear},
    tags={ModelTag.regressor},
    description='The Passive Aggressive Regressor is a linear model from the scikit-learn library. It is an online learning algorithm particularly suitable for large-scale data and streaming data scenarios where the model is incrementally updated with new data points. The algorithm derives its name from its approach to updating the model\'s weights: it is "passive" when the current model\'s prediction error is within a specified margin (controlled by the epsilon parameter), and "aggressive" when the prediction error exceeds this margin. The aggressiveness of the weight updates is controlled by a regularization parameter, which balances the trade-off between model stability and adaptability to new data. The Passive Aggressive Regressor is computationally efficient and can handle high-dimensional feature spaces, making it a valuable choice for various regression tasks, such as predicting numerical values in time-series data, forecasting sales, or estimating user ratings in recommendation systems.',
    advantages=[
        "Efficient for large-scale learning tasks",
        "Suitable for online learning and streaming data",
        "Can handle high-dimensional data",
        "Supports early stopping to prevent overfitting",
    ],
    disadvantages=[
        "Sensitive to feature scaling",
        "Requires tuning of hyperparameters",
        "May not perform well on small datasets",
    ],
    prime=[],
    display_name="Passive Aggressive Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
