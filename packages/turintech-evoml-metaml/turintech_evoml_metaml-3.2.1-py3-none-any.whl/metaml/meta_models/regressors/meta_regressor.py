import pandas as pd
from scipy import stats
from abc import abstractmethod
from sklearn.metrics import r2_score
from typing import Optional, Sequence


from metaml.meta_models.meta_model import MetaModel
from metaml._util.target_transformers.power_target_transformer import (
    TargetPowerTransformer,
)
from metaml.meta_models.metadata import ModelTag
from metaml.uncertainty_models.base import UncertaintyModel


class MetaRegressor(MetaModel):
    """This is the parent class for all regression meta-models available in MetaML"""

    _estimator_type: str = ModelTag.regressor
    _target_transformer: TargetPowerTransformer
    _skewness_threshold: float = 5.0
    _auto_target_transform: bool = True
    _target_transformed: bool = False
    uncertainty_model: Optional[UncertaintyModel]

    def has_predict_proba(self) -> bool:
        """Checks if the model has a predict_proba method.

        Returns:
            False for regressor models.
        """
        return False

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit the model according to the given training data. If the skewness of the target crosses a threshold then the
        target will be transformed.

        Args:
            X (pd.DataFrame): dataframe of shape (n_samples, n_features) containing features of the training samples.
            y (pd.Series): series of shape (n_samples,) containing the labels of the samples in X.

        """
        if self._auto_target_transform and self._skewness_threshold < abs(stats.skew(y.to_numpy())):
            self._target_transformer = TargetPowerTransformer()
            self._target_transformer.fit(y)
            y_transformed = pd.Series(self._target_transformer.transform(y))
            y_transformed.index = y.index
            self._fit(X, y_transformed)
            self._target_transformed = True
        else:
            self._fit(X, y)

        self.fitted_ = True

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Obtain model predictions for the given features.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) providing features of samples which will be
             labelled.

        Returns:
            predictions (pd.Series): labels for the given samples.

        """
        predictions = self._predict(X)
        if self._target_transformed:
            predictions = self._target_transformer.inverse_transform(predictions)
        return pd.Series(predictions, index=X.index)

    def score(self, X: pd.DataFrame, y_true: pd.Series) -> float:
        """Return the R^2 score of the performance of the trained model on supplied data.

        Args:
            X (pd.DataFrame): Features of the training data.
            y (pd.Series): Target vector.


        Returns:
            score (float): The R^2 score of the model on the supplied data.

        """

        return r2_score(y_true, self.predict(X))

    @abstractmethod
    def _fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) containing the features of each sample of
            training data.
            y (pd.Series): A series of shape (n_samples,) containing the target values of the samples in X.

        """
        """Library specific implementation of _fit for regression models."""

    @abstractmethod
    def _predict(self, X: pd.DataFrame) -> pd.Series:
        """Library specific implementation of _predict for regression models."""

    def set_uncertainty_model(self, uncertainty_model: UncertaintyModel) -> None:
        """
        Set the uncertainty model of the meta regressor.

        This method allows for the specification of the uncertainty model used by the meta regressor for generating
        prediction intervals. The uncertainty model should be a fitted instance of a subclass of the ResidualModel abstract base class.

        Args:
            uncertainty_model (UncertaintyModel): A fitted instance of a subclass of ResidualModel.

        Raises:
            ValueError: If the provided uncertainty model is not an instance of ResidualModel.
        """
        if not isinstance(uncertainty_model, UncertaintyModel):
            raise ValueError(
                f"uncertainty_model must be an instance of ResidualModel, but got {type(uncertainty_model)}"
            )
        self.uncertainty_model = uncertainty_model

    def fit_uncertainty_model(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Fit the uncertainty model according to the given training data.

        Args:
            X (pd.DataFrame): dataframe of shape (n_samples, n_features) containing features of the training samples.
            y (pd.Series): series of shape (n_samples,) containing the labels of the samples in X.

        Raises:
            ValueError: If the uncertainty model is not defined.
        """
        if self.uncertainty_model is None:
            raise ValueError("Residual model is not defined. Please define a uncertainty model.")

        # Compute residuals
        residuals = y - self.predict(X)

        # Fit residual model
        self.uncertainty_model.fit(X, residuals)

    def predict_interval(self, X: pd.DataFrame, quantiles: Sequence[float]) -> pd.DataFrame:
        """
        Obtain prediction intervals for the given features.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) providing features of samples which will be
             labelled.
            quantiles (Sequence[float]): Quantiles for prediction intervals.

        Returns:
            intervals (pd.DataFrame): Prediction intervals for the given samples.

        Raises:
            ValueError: If the uncertainty model is not fitted.
        """
        if self.uncertainty_model is None:
            raise ValueError(
                "Residual model is not defined. Please define an uncertainty model and re-fit the meta model."
            )
        if not self.fitted_:
            raise ValueError("Model is not fitted. Please fit the model before predicting intervals.")

        predictions = self.predict(X)
        prediction_intervals = self.uncertainty_model.predict_interval(X, quantiles)

        # adjust intervals by adding predictions
        prediction_intervals = prediction_intervals.add(predictions, axis=0)

        return prediction_intervals
