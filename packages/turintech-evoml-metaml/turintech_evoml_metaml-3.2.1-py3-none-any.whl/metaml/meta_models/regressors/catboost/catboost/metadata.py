from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import RegressorName


metadata = MetaData(
    model_name=RegressorName.catboost_regressor,
    model_type={ModelTypeEnum.tree, ModelTypeEnum.ensemble},
    tags={ModelTag.regressor},
    description="The CatBoost Regressor is an implementation of gradient boosting for decision trees, specifically designed to handle categorical features effectively. CatBoost stands for 'Categorical Boosting' and is optimized to reduce overfitting and improve generalization. The model is known for its robustness and high performance in a variety of data settings, including imbalanced and sparse datasets. It incorporates multiple techniques like ordered boosting and oblivious trees to improve speed and predictive accuracy.",
    advantages=[
        "Handling of Categorical Features: One of the standout features of CatBoost is its native ability to handle categorical variables, removing the need for prior encoding and thereby preventing data leakage and dimensionality increase.",
        "Robust to Overfitting: CatBoost incorporates built-in mechanisms to prevent overfitting, making it more robust for small datasets or datasets where the number of features is high compared to the number of samples.",
        "High Performance: CatBoost is often cited for its superior performance in terms of predictive accuracy, outperforming other gradient boosting and tree-based methods in various benchmarks.",
    ],
    disadvantages=[
        "Computational Complexity: CatBoost can be computationally intensive and may require longer training times compared to simpler models, especially on large datasets.",
        "Hyperparameter Tuning: While CatBoost is known for good 'out-of-the-box' performance, fine-tuning its numerous hyperparameters for optimal performance can be time-consuming and complex.",
        "Interpretability: Although it provides some tools for interpretation like feature importances, CatBoost models are generally more difficult to interpret compared to linear models due to their ensemble nature.",
    ],
    prime=[],
    display_name="CatBoost Regressor",
    supports=Supports(probabilities=False, feature_importances=True),
)
