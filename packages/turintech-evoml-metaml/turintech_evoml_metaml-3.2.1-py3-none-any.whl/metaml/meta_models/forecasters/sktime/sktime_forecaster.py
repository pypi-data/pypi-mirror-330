import pandas as pd
import numpy as np
from typing import Sequence, Tuple, Set
from sktime.forecasting.base import ForecastingHorizon, BaseForecaster


from metaml.meta_models.forecasters.meta_forecaster import MetaForecaster
from metaml.meta_models.forecasters.time_frame import TimeFrame, IdentifierType, IndexTypeEnum


class LibSKTimeForecaster(MetaForecaster):
    """
    Forecasting wrapper class for sktime models.

    This class provides an interface for using sktime forecasting models within the metaml forecasting
    framework. It supports fitting, predicting, and updating models with single time series data.

    Currently, only single series is supported with sktime forecasters.

    Attributes:
        model (BaseForecaster): The sktime forecasting model.
    """

    model: BaseForecaster

    # Fit and update method and associated helper methods
    # ------------------------------------------------------------------------------------------------------------------
    def _fit(self, observed_data: TimeFrame) -> None:
        """
        Fit the model with the observed data.

        This method fits the sktime forecasting model to the training data. If the training data contains multiple
        series with different step sizes, it raises a ValueError.

        Raises:
            ValueError: If the observed data contains multiple step sizes. This is currently not supported by sktime.
        """
        # Extract the unique step sizes from the observed data
        unique_step_sizes = set(observed_data.step_sizes.values())

        # Check if there's more than one unique step size
        if len(unique_step_sizes) != 1:
            raise ValueError(
                "At present we can only train sktime forecasters on time series which share the same step size."
            )

        # Prepare the data for fitting the model
        y, X_future = self._prepare_observations_for_fit_and_update()

        # Fit the model
        # If there are no future covariates, fit the model only on the target series
        if X_future.empty:
            self.model.fit(y)
        else:
            # If there are future covariates, fit the model on both the target series and the covariates
            self.model.fit(y, X=X_future)

    def _update(self) -> None:
        """
        Update the forecasting models specific to sktime.

        This function fetches the subseries corresponding to the unique identifier, retrieves the target series
        and covariates series from the subseries, and then prepares these data for the sktime model. The model is
        updated with the prepared data without updating the model parameters.
        """
        y, X_future = self._prepare_observations_for_fit_and_update()

        # Update the model
        if X_future.empty:
            self.model.update(y=y, update_params=True)
        else:
            self.model.update(y=y, X=X_future, update_params=True)

    def _convert_index_col_to_period(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Convert index column to period format for a given DataFrame.

        This method takes a DataFrame, groups it by identifier columns and converts the index column
        of each group to a period index.

        Args:
            data (pd.DataFrame): A DataFrame with an index column containing timestamps.

        Returns:
            pd.DataFrame: A new DataFrame with the index column converted to a period format.
        """
        # Copy the DataFrame to avoid mutating the original data
        data = data.copy()

        for identifier, group in data.groupby(self.observed_data.identifier_cols):
            # Define the period index for each group based on its frequency and convert to period index
            period_index = pd.DatetimeIndex(
                group[self.observed_data.index_col], freq=self.observed_data.step_sizes[identifier]
            ).to_period()

            # Replace the old index with the new period index
            data.loc[group.index, self.observed_data.index_col] = period_index

        # Return the DataFrame with the updated index
        return data

    def _prepare_observations_for_fit_and_update(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Prepare the observed data for fitting and updating the model.

        If the index type of the observed data is DATETIME, it converts the index column to period format for better
        compatibility with sktime. The method then sets the appropriate index and separates the data into target series
        and covariates series.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two DataFrames. The first DataFrame (y) represents the
            target series, and the second DataFrame (X_future) represents the covariate series.
        """
        # Convert the index column to period format if the index type is DATETIME
        if self.observed_data.index_type == IndexTypeEnum.DATETIME:
            observed_df = self._convert_index_col_to_period(self.observed_data.data)
        else:
            observed_df = self.observed_data.data

        # Set the appropriate index
        observed_df = observed_df.set_index(self.observed_data.identifier_cols + [self.observed_data.index_col])

        # Separate the data into target series and covariates series
        y = observed_df[[self.target_name]].dropna()
        X_future = observed_df[self.future_covariate_names].dropna()

        return y, X_future

    # Predict method and helper methods
    # ------------------------------------------------------------------------------------------------------------------
    def _predict(self, n: int, inference_data: TimeFrame) -> TimeFrame:
        """
        Obtain a forecast from and sktime forecaster.

        This method obtains a forecast for the time series based on the exogenous variables contained in `inference_data`.

        Args:
            n (int): Number of steps ahead to forecast.
            inference_data (TimeFrame): TimeFrame containing the exogenous variables for the time steps for
                which we wish to obtain forecasts. The time index is stored by the index of the dataframe.

        Returns:
            TimeFrame: A TimeFrame containing the forecast target values. The TimeFrame will have a multi-index
                constructed from the identifiers and time index.

        The method works as follows:
            1. It creates a relative forecasting horizon for the sktime model.
            2. It prepares the future covariates dataframe, with a multi-index constructed from the identifiers
               and time index.
            3. It obtains the predictions from the sktime model.
            4. It filters the predictions to only include the requested series.
            5. It validates the period index and replaces it with the original datetime index.
            6. It returns a TimeFrame containing the forecast target values.

        """
        # Specify the steps of the forecast relative to the last target value in the training data
        forecasting_horizon_relative = np.arange(1, n + 1)

        # A relative forecasting horizon is created for the sktime model
        forecasting_horizon = ForecastingHorizon(forecasting_horizon_relative, is_relative=True)

        # Prepare the future covariates dataframe with a multi-index constructed from the identifiers and time index
        future_covariates_dataframe = self._prepare_future_covariates_df(
            inference_data=inference_data, forecast_horizon_relative=forecasting_horizon_relative
        )

        # Obtain the predictions
        if future_covariates_dataframe.empty:
            predictions = self.model.predict(forecasting_horizon)
        else:
            predictions = self.model.predict(forecasting_horizon, X=future_covariates_dataframe)

        # Reset the multi-index so the identifiers and time index are columns
        predictions = predictions.reset_index()

        # Validate the period index and replace it with the original datetime index
        if self.observed_data.index_type == IndexTypeEnum.DATETIME:
            predictions = self._validate_period_index(predictions, forecasting_horizon_relative)

        return TimeFrame(
            data=predictions,
            index_col=self.observed_data.index_col,
            identifier_cols=self.observed_data.identifier_cols,
            step_sizes=self.observed_data.step_sizes,
        )

    def _prepare_future_covariates_df(
        self, inference_data: TimeFrame, forecast_horizon_relative: Sequence[int]
    ) -> pd.DataFrame:
        """
        Extract future covariates from the inference data.

        Args:
            inference_data (TimeFrame): A TimeFrame object containing the exogenous variables.
            forecast_horizon_relative (Sequence[int]): The sequence of forecasting steps ahead.

        Returns:
            pd.DataFrame: DataFrame of future covariates.
        """

        # Compute time index
        time_index = self.get_forecast_horizon_absolute(forecast_horizon_relative=forecast_horizon_relative)
        series_id = self.observed_data.series_ids[0]

        # Get slice of inference data and select only future covariate columns
        return (
            inference_data.get_slice_by_time(series_ids=series_id, start=time_index[0], stop=time_index[-1])[
                self.future_covariate_names
            ].data
        ).set_index(self.observed_data.identifier_cols + [self.observed_data.index_col])

    def _validate_period_index(self, predictions: pd.DataFrame, forecast_horizon_relative: np.ndarray) -> pd.DataFrame:
        """
        Validate and adjust period index of the given predictions DataFrame.

        This method checks if the index of the given predictions matches the expected forecast time index values.
        If the index does not match, it raises an error. If the observed data index type is DATETIME, it converts the
        index to datetime format.

        Args:
            predictions (pd.DataFrame): DataFrame containing the prediction values.
            forecast_horizon_relative (np.ndarray): Array of forecast horizon steps.

        Returns:
            pd.DataFrame: DataFrame with validated and adjusted index.

        Raises:
            IndexError: If the index of the predictions does not match the expected forecast time index values.
        """
        for identifier, group in predictions.groupby(self.observed_data.identifier_cols):
            datetime_index = pd.DatetimeIndex(
                self.observed_data.get_time_index(
                    series_id=identifier,
                    step_index=self.latest_target_step_index + forecast_horizon_relative,
                ),
                freq=self.observed_data.step_sizes[identifier],
            )
            period_index = pd.PeriodIndex(predictions.loc[group.index, self.observed_data.index_col])

            if not datetime_index.to_period().equals(period_index):
                raise IndexError("The index of the predictions does not match the expected forecast time index values.")

            predictions.loc[group.index, self.observed_data.index_col] = datetime_index

        predictions[self.observed_data.index_col] = pd.to_datetime(predictions[self.observed_data.index_col])

        return predictions
