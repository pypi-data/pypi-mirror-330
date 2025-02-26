import numpy as np
import pandas as pd


from metaml.exceptions import TargetTransformerException


from sklearn.preprocessing import PowerTransformer
from typing import Union
from enum import Enum


class Method(str, Enum):
    yeo_johnson = "yeo-johnson"
    box_cox = "box-cox"


def standardise_input(y: Union[np.ndarray, pd.Series]) -> np.ndarray:
    """Check the target has a single column and convert input to numpy array."""

    if isinstance(y, pd.Series):
        y = y.to_numpy()

    if not y.ndim == 1:
        raise TargetTransformerException("Expected 1 column of input. Instead received {} columns.".format(y.shape[1]))

    return y


class TargetPowerTransformer(PowerTransformer):
    min_y: float
    max_y: float

    def __init__(self):
        super().__init__(standardize=True, method=Method.yeo_johnson, copy=True)

    def fit(self, y: Union[np.ndarray, pd.Series]):
        """Fit the transformation and store minimum and maximum values for imputing out of range values."""

        y = standardise_input(y)

        self.min_y = min(y)
        self.max_y = max(y)
        super().fit(y.reshape(-1, 1))

    def transform(self, y: Union[np.ndarray, pd.Series]) -> np.ndarray:
        """Transform the target."""

        y = standardise_input(y)

        return super().transform(y.reshape(-1, 1))[:, 0]

    def inverse_transform(self, y_transformed: Union[np.ndarray, pd.Series]) -> np.ndarray:
        """Invert the transformation of the target and carry out imputation for out of range values."""

        y_transformed = standardise_input(y_transformed)

        y = super().inverse_transform(y_transformed.reshape(-1, 1))[:, 0]

        less_than_min = np.full(y_transformed.shape, False)
        greater_than_max = np.full(y_transformed.shape, False)

        lambda_ = self.lambdas_[0]  # there exists only one lambda

        # valid for yeo-johnson method
        if lambda_ < 0:
            greater_than_max = y_transformed >= -1 / lambda_
        if lambda_ > 2:
            less_than_min = y_transformed <= -1 / lambda_

        y[less_than_min] = self.min_y
        y[greater_than_max] = self.max_y

        return y
