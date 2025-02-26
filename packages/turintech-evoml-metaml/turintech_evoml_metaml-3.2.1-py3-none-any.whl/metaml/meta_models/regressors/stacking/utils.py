from dataclasses import dataclass, field
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.metrics import make_scorer, f1_score
from scipy.stats import loguniform


class FeatureSetReducer(str, Enum):
    mrmr = "mrmr"
    pca = "pca"
    umap = "umap"
    kmeans = "kmeans"
    kmeans_distance = "kmeans_distance"


class BaseSetReducer(str, Enum):
    mrmr = "mrmr"


class StackingStrategy(str, Enum):
    # Stack initial training matrix (combined) or not (basic)
    basic = "basic"
    combined = "combined"


class RelevanceMetricClassification(str, Enum):
    # Relevance metric for mrmr
    fStatistic = "f"
    randomForest = "rf"
    f1 = "f1"


class RelevanceMetricRegression(str, Enum):
    # Relevance metric for mrmr
    fStatistic = "f"
    randomForest = "rf"


@dataclass
class StackingOptions:
    # Fixing this for all
    random_state: int = 42
    cv_: int = 5


def calculate_number_features(n: int) -> int:
    """
    A simple function to determine the number of features to select for mrmr.
    """
    if n <= 0:
        raise ValueError(f"Initial number of features given is not positive: {n}.")
    if n == 1:
        return 1
    return round(np.log2(n))


def f1_score_mrmr(X: pd.DataFrame, y: pd.Series):
    """
    Calculates f1 score of each of the columns in X with y. It can be used
    as a relevance function for mrmr.
    """
    from sklearn.metrics import f1_score

    scores = pd.Series(0.0, X.columns)
    for col in X:
        scores[col] = f1_score(X[col], y, average="macro")
    return scores
