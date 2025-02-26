import pandas as pd
import numpy as np
from abc import abstractmethod
from typing import List, Optional, Sequence, Union, Iterable, Tuple, Type, TypeVar


from metaml.meta_models.meta_model import MetaModel
from metaml.meta_models.forecasters.time_frame import TimeFrame, IdentifierType
from metaml.exceptions import MissingDataException


SeriesType = Union[pd.DataFrame, TimeFrame]
SeriesTypeVar = TypeVar("SeriesTypeVar", pd.DataFrame, TimeFrame)


class MetaForecaster(MetaModel):
    """This is the parent class for all forecasting meta-models available in MetaML"""

    observed_data: TimeFrame
    """Keeps a record of the training data and any data supplied during updates.
    This should only be altered by the fit, update, update_predict and update_predict_rolling window methods."""

    target_name: str
    future_covariate_names: List[str] = []
    past_covariate_names: List[str] = []

    # Fit and update methods
    # ------------------------------------------------------------------------------------------------------------------
    def fit(
        self,
        y: pd.Series,
        X_future: Optional[pd.DataFrame] = None,
        X_past: Optional[pd.DataFrame] = None,
    ) -> None:
        """Fit the model to the given training data.

        Args:
            y (SeriesType): The time series we intend to forecast. This should be univariate.
            X_future (Optional[SeriesType]): SeriesType containing the exogenous variables which are known in
                advance.
            X_past (Optional[SeriesType]): SeriesType containing the exogenous variables which are only known
                after being observed.

        Raises:
            ValueError: If target_series is not univariate.
            MissingDataException: If any of the supplied past or future covariates do not cover the entire target
                series.
        """

        y, X_future, X_past = self._cast_to_time_frame(y, X_future, X_past)

        if len(y.series_ids) > 1:
            raise NotImplementedError("Multivariate time series are not yet supported.")

        uid = y.series_ids[0]
        if X_past is not None and X_past.last_observed_time_indexes[uid] < y.last_observed_time_indexes[uid]:
            raise MissingDataException("The supplied past covariates must cover the entire target series.")
        if X_future is not None and X_future.last_observed_time_indexes[uid] < y.last_observed_time_indexes[uid]:
            raise MissingDataException("The supplied future covariates must cover the entire target series.")

        if len(y.data_cols) != 1:
            raise ValueError("The target series must be univariate.")
        self.target_name = y.data_cols[0]

        self.future_covariate_names = X_future.data_cols if X_future is not None else []
        self.past_covariate_names = X_past.data_cols if X_past is not None else []

        self.observed_data = y.copy()
        if X_future is not None:
            self.observed_data = self.observed_data.merge(X_future)
        if X_past is not None:
            self.observed_data = self.observed_data.merge(X_past)

        self._fit(observed_data=self.observed_data)

    def _cast_to_time_frame(
        self,
        y: pd.Series,
        X_future: Optional[pd.DataFrame] = None,
        X_past: Optional[pd.DataFrame] = None,
    ) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        y = y.to_frame()
        y = TimeFrame.from_indexed_frame(y)

        if X_future is not None:
            X_future = TimeFrame.from_indexed_frame(X_future)

        if X_past is not None:
            X_past = TimeFrame.from_indexed_frame(X_past)

        return y, X_future, X_past

    def update(
        self,
        y: Optional[pd.Series] = None,
        X_future: Optional[pd.DataFrame] = None,
        X_past: Optional[pd.DataFrame] = None,
    ) -> None:
        """Update the model according to the given training data.

        Args:
            y (Optional[SeriesType]): SeriesType containing the time series we intend to forecast.
            X_future (Optional[SeriesType]): SeriesType containing exogenous variables which are known in
                advance.
            X_past (Optional[SeriesType]): SeriesType containing exogenous variables which are only known after
                being observed.

        """

        y, X_future, X_past = self._cast_to_time_frame(y, X_future, X_past)

        if y is not None:
            self.observed_data = self.observed_data.merge(y)
        if X_future is not None:
            self.observed_data = self.observed_data.merge(X_future)
        if X_past is not None:
            self.observed_data = self.observed_data.merge(X_past)
        self._update()

    @abstractmethod
    def _update(self) -> None:
        """Library specific implementation of _update for forecasting models."""

    @abstractmethod
    def _fit(self, observed_data: TimeFrame) -> None:
        """Library specific implementation of _fit for forecasting models.

        Args:
            observed_data (TimeFrame): The training data to fit the model to, including the target series, past and
            future covariates, and the time index.

        """

    # Predict methods
    # ------------------------------------------------------------------------------------------------------------------
    def predict(
        self,
        n: int,
        X_future: Optional[pd.DataFrame] = None,
    ) -> pd.Series:
        """
        Generate a forecast for the specified series.

        Args:
            n (int): The number of forecast steps to take beyond the last known time index.
            X_future (Optional[SeriesType]): A SeriesType of future covariates spanning the forecast horizon.

        Returns:
            SeriesType: The generated forecast.

        Raises:
            KeyError: If any of the supplied series_ids are not present in the training data.
        """

        if X_future is not None:
            if len(self.observed_data.series_ids) != 1:
                raise NotImplementedError("Multiple time series are not yet supported.")
            X_future[self.observed_data.identifier_cols] = self.observed_data.series_ids[0]
            X_future = X_future.reset_index()
            inference_data = self.observed_data.merge(X_future)
        else:
            inference_data = self.observed_data.copy()

        if n <= 0:
            raise ValueError("The number of forecast steps 'n' must be a positive integer.")

        predictions = self._predict(n, inference_data=inference_data)

        # Validation
        series_id = predictions.series_ids[0]
        predictions_series = predictions.get_series(series_ids=series_id)
        self._validate_forecast(predictions=predictions_series, n=n)

        predictions = predictions_series.get_series_df(series_id).squeeze(axis=1)

        return predictions

    @abstractmethod
    def _predict(self, n: int, inference_data: TimeFrame) -> TimeFrame:
        """Library specific implementation of _predict for forecasting models."""

    def _validate_forecast(self, predictions: TimeFrame, n: int) -> None:
        """Check that the index of the forecast values matches the expected forecast horizon."""
        forecast_horizon_absolute = self.get_forecast_horizon_absolute(forecast_horizon_relative=np.arange(1, n + 1))
        if not all(predictions.index == forecast_horizon_absolute):
            raise IndexError("Mismatch in forecast index and expected horizon.")

    # Combined update and predict method
    # ------------------------------------------------------------------------------------------------------------------
    def update_predict(
        self,
        n: int,
        y: pd.Series,
        X_past: Optional[pd.DataFrame] = None,
        X_future: Optional[pd.DataFrame] = None,
    ) -> pd.Series:
        # Update the model with new data
        self.update(
            y=y,
            X_past=X_past,
            X_future=X_future,
        )
        return self.predict(n=n)

    # Rolling window prediction method and associated helper methods
    # ------------------------------------------------------------------------------------------------------------------
    def update_predict_rolling_window(
        self,
        n: int,
        y: pd.Series,
        X_future: Optional[pd.DataFrame] = None,
        X_past: Optional[pd.DataFrame] = None,
    ) -> SeriesType:
        """
        Given the last observation in the training data, generate rolling window predictions
        of length `n` until the end of the newly supplied target series.

        Args:
            n (int): Length of the forecast.
            y (SeriesType): Target series data.
            X_future (Optional[SeriesType]): Future covariates data.
            X_past (Optional[SeriesType]): Past covariates data.

        Returns:
            SeriesType: SeriesType object with the collected predictions.
        """

        y, X_future, X_past = self._cast_to_time_frame(y, X_future, X_past)

        # Merge all data into a single TimeFrame
        data_list = [self.observed_data, y]
        if X_future is not None:
            data_list.append(X_future)
        if X_past is not None:
            data_list.append(X_past)
        combined_data = TimeFrame.merge_list(data_list)

        # Iterate over series and get predictions
        predictions = self._update_predict_series(y.series_ids[0], combined_data, n, X_future)

        # Cast to the desired output type
        return predictions.to_indexed_frame()[self.target_name]

    def _update_predict_series(
        self,
        series_id: IdentifierType,
        combined_data: TimeFrame,
        n: int,
        future_covariates: Optional[TimeFrame] = None,
    ) -> TimeFrame:
        """
        Generate predictions for a single series within the combined data.

        Args:
            series_id (IdentifierType): Unique identifier for the series.
            combined_data (TimeFrame): Combined data for all series.
            n (int): Length of the forecast.
            future_covariates (Optional[TimeFrame]): Future covariates data.

        Returns:
            TimeFrame: TimeFrame object with the predictions for a single series.
        """

        # Get necessary indices and data for the series
        series_data, step_index_latest_observed, step_index_last_forecast = self._get_series_info(
            series_id, combined_data
        )
        num_forecast_windows = step_index_last_forecast - step_index_latest_observed - n + 1
        if num_forecast_windows <= 0:
            raise MissingDataException(f"Not enough data to make forecasts for series {series_id}.")

        # Generate predictions for each forecast window
        collected_series_predictions = [
            self._update_predict_single_window(
                series_id,
                series_data,
                f_idx,
                step_index_latest_observed,
                n,
                future_covariates,
            )
            for f_idx in range(num_forecast_windows)
        ]

        # Merge all series predictions into a single TimeFrame
        return TimeFrame.concatenate_list(collected_series_predictions)

    def _update_predict_single_window(
        self,
        series_id: IdentifierType,
        series_data: TimeFrame,
        window_idx: int,
        step_index_latest_observed: int,
        n: int,
        future_covariates: Optional[TimeFrame] = None,
    ) -> TimeFrame:
        """
        Generate a forecast for a single window of a time series.

        This method generates a forecast for the time window starting at
        the position indicated by `f_idx` in the given time series data.
        The forecast is validated and the window identifier is added
        before returning.

        Args:
            series_id (IdentifierType): The identifier of the time series to forecast.
            series_data (TimeFrame): The complete time series data.
            window_idx (int): The index of the forecast window.
            step_index_latest_observed (int): The step index of the latest observed time index in the series data.
            n (int): The length of the forecast horizon.
            future_covariates (Optional[TimeFrame]): A time frame of future covariates to use for the forecast.

        Returns:
            TimeFrame: The forecasted time series for the specified window, including an identifier for the forecast
            window.
        """
        # Get the time at which the next forecast window will be made
        current_time = series_data.get_time_index(series_id, window_idx + step_index_latest_observed)

        # Get all the data up to the current time
        past_data = series_data.get_slice_by_time(series_ids=series_id, stop=current_time)
        target_series = past_data[[self.target_name]]
        past_covariates = past_data[self.past_covariate_names]

        # Call the helper function to make the forecast
        predictions = self.update_predict(
            n=n,
            y=target_series.to_indexed_frame()[self.target_name],
            X_past=past_covariates.to_indexed_frame(),
            X_future=future_covariates.to_indexed_frame() if future_covariates is not None else None,
        )
        predictions = TimeFrame.from_indexed_frame(predictions.to_frame())

        # Check that the index of the forecast values matches the expected forecast horizon
        self._validate_forecast(predictions=predictions, n=n)

        # Add the forecast window identifier and append to list
        predictions = predictions.add_identifier(identifier_name="window_idx", identifier_value=window_idx)

        return predictions

    def _get_series_info(self, series_id: IdentifierType, combined_data: TimeFrame) -> Tuple[TimeFrame, int, int]:
        """
        Extracts the series data and relevant indices for a given series.

        Args:
            series_id (IdentifierType): Unique identifier for the series.
            combined_data (TimeFrame): Combined data for all series.

        Returns:
            tuple: Tuple containing the series data, the index of the latest observation, and the index of the last
                forecast.
        """
        series_data = combined_data.get_series(series_id)
        latest_target_time_index_in_training_data = self.latest_target_time_index

        step_index_latest_observed = series_data.get_step_index(
            series_id=series_id, time_index=latest_target_time_index_in_training_data
        )
        step_index_last_forecast = series_data.get_step_index(
            series_id=series_id, time_index=series_data.index.iloc[-1]
        )

        return series_data, step_index_latest_observed, step_index_last_forecast

    # Frame of reference methods. These methods answer the following questions:
    # - What time is it from the forecaster's perspective?
    # - What is time will it be `n` steps into the future?
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def latest_target_time_index(self):
        """Returns the time index of the last observation."""
        series_id = self.observed_data.series_ids[0]
        return self.observed_data.get_time_index(series_id, self.latest_target_step_index)

    @property
    def latest_target_step_index(self):
        """Returns a dictionary mapping each series_id to the step index of the last observation for the corresponding
        subseries.
        """
        series_id = self.observed_data.series_ids[0]
        return self.observed_data.get_series_df(series_id)[self.target_name].reset_index(drop=True).last_valid_index()

    def get_forecast_horizon_absolute(
        self, forecast_horizon_relative: Sequence[int]
    ) -> Union[Sequence[int], Sequence[pd.Timestamp]]:
        """
        Calculate and return absolute forecast horizon based on relative horizon and series ID.

        This method converts a relative forecast horizon (e.g., [1, 2, 3]) to absolute values by adding the relative
        horizon to the observed step index of the given series and converting the step index to a time index.

        Args:
            forecast_horizon_relative (Sequence[int]): Relative forecast horizon.

        Raises:
            TypeError: If `forecast_horizon_relative` is not iterable.
            TypeError: If `forecast_horizon_relative` does not contain only integers.

        Returns:
            Union[Sequence[int], Sequence[pd.Timestamp]]: The absolute forecast horizon.
                The return type depends on the time index type of the observed data.
                For integer-indexed time series, the return type is Sequence[int];
                for timestamp-indexed time series, the return type is Sequence[pd.Timestamp].
        """
        series_id = self.observed_data.series_ids[0]

        # Validate forecast_horizon_relative
        if not isinstance(forecast_horizon_relative, Iterable):
            raise TypeError("`forecast_horizon_relative` must be an iterable.")

        if not all(np.issubdtype(type(i), np.integer) for i in forecast_horizon_relative):
            raise TypeError("`forecast_horizon_relative` must be a sequence of integers.")

        return self.observed_data.get_time_index(
            series_id=series_id,
            step_index=self.latest_target_step_index + forecast_horizon_relative,
        )

    # Other methods
    # ------------------------------------------------------------------------------------------------------------------
    def score(self, *args, **kwargs):
        raise NotImplementedError("The score method is not yet implemented for forecasters.")

    def has_predict_proba(self) -> bool:
        """
        Metaml does not support predict_proba for forecasters.

        Returns:
            False

        """
        return False
