from typing import List, Tuple, Optional
from darts import TimeSeries
from abc import abstractmethod
import pandas as pd


from metaml.meta_models.forecasters.meta_forecaster import MetaForecaster
from metaml.meta_models.forecasters.time_frame import TimeFrame, IdentifierType


class LibDartsForecaster(MetaForecaster):
    def _fit(self, observed_data: TimeFrame) -> None:
        # Extract target series and covariates
        target_series, past_covariates, future_covariates = self._extract_time_series(
            data=observed_data,
        )

        self._fit_model(
            target_series=target_series,
            past_covariates=past_covariates,
            future_covariates=future_covariates,
        )

    @abstractmethod
    def _fit_model(
        self,
        target_series: TimeSeries,
        past_covariates: Optional[TimeSeries] = None,
        future_covariates: Optional[TimeSeries] = None,
    ) -> None:
        """
        Calls LibDartsForecaster.model.fit and passes the relevant data.

        Args:
            target_series (TimeSeries): List of target time series data.
            past_covariates (Optional[TimeSeries]): Optional list of past covariates time series data.
            future_covariates (Optional[TimeSeries]): Optional list of future covariates time series data.
        """

    def _update(self):
        """All the update logic for darts forecasters is already performed by updating MetaForecaster._observed_data.
        If we support online learning in future then we will need to implement the necessary logic here."""
        ...

    def _extract_time_series(
        self,
        data: TimeFrame,
    ) -> Tuple[TimeSeries, Optional[TimeSeries], Optional[TimeSeries]]:
        """
        Extract the target, past covariates and future covariates from the given data and convert them into separate TimeSeries objects.

        Args:
            data (TimeFrame): The data frame to be used for training or inference.

        Returns:
            Tuple[TimeSeries, Optional[TimeSeries], Optional[TimeSeries]]:
            A tuple containing three lists of TimeSeries objects: target series, past covariates,
            and future covariates. If past or future covariates are not present, those lists will be None.

        """

        series_id = data.series_ids[0]
        target_series = TimeSeries.from_series(data.get_series_df(series_id)[self.target_name].dropna())
        past_covariates = (
            TimeSeries.from_dataframe(data.get_series_df(series_id)[self.past_covariate_names].dropna())
            if self.past_covariate_names
            else None
        )
        future_covariates = (
            TimeSeries.from_dataframe(data.get_series_df(series_id)[self.future_covariate_names])
            if self.future_covariate_names
            else None
        )

        return target_series, past_covariates, future_covariates

    def _construct_predictions_frame(self, predictions: TimeSeries) -> TimeFrame:
        """
        Constructs a TimeFrame of predictions from a list of tuples containing identifiers and predictions in TimeSeries
        format.

        Args:
            predictions (TimeSeries): A list of tuples, each containing a unique identifier
                and the corresponding TimeSeries object of predictions.

        Returns:
            TimeFrame: A TimeFrame object containing the predictions.

        """

        # Create a list to store DataFrames
        dataframes_list = []
        step_sizes = {}

        series_id = self.observed_data.series_ids[0]

        # Get a DataFrame of predictions and mov the index to be a column
        prediction_df = predictions.pd_dataframe().reset_index(names=self.observed_data.index_col)

        # Add the identifier column
        prediction_df[self.observed_data.identifier_cols] = series_id

        # Append the DataFrame to dataframes_list
        dataframes_list.append(prediction_df)

        step_sizes[series_id] = self.observed_data.step_sizes[series_id]

        # Concatenate all predictions into a single DataFrame
        all_predictions_df = pd.concat(dataframes_list, axis=0)

        return TimeFrame(
            all_predictions_df,
            index_col=self.observed_data.index_col,
            identifier_cols=self.observed_data.identifier_cols,
            step_sizes=step_sizes,
        )

    def _predict(self, n: int, inference_data: TimeFrame) -> TimeFrame:
        """
        Predict the next n time steps.

        Args:
            n (int): The number of time steps to forecast.
            inference_data (TimeFrame): The data to make predictions on.
            series_ids (List[IdentifierType]): A list of unique identifiers for the series.

        Returns:
            TimeFrame: TimeFrame object containing the predictions.
        """
        # Extract target series and covariates.
        target_series, past_covariates, future_covariates = self._extract_time_series(
            data=inference_data,
        )

        # Generate predictions. The predictions are returned as a list with the same order as the series_ids_list.
        predictions = self._model_predict(n, target_series, past_covariates, future_covariates)

        # Construct and return predictions time series frame
        return self._construct_predictions_frame(predictions=predictions)

    @abstractmethod
    def _model_predict(
        self,
        n: int,
        target_series: TimeSeries,
        past_covariates: Optional[TimeSeries],
        future_covariates: Optional[TimeSeries],
    ) -> TimeSeries:
        """
        Pass the required data to LibDartsForecaster.model.predict and return the predictions.

        Args:
            n (int): The number of time steps to forecast.
            target_series (TimeSeries): List of target time series data.
            past_covariates (Optional[TimeSeries]): Optional list of past covariates time series data.
            future_covariates (Optional[TimeSeries]): Optional list of future covariates time series data.

        Returns:
            TimeSeries: TimeSeries containing predictions.

        """
        ...
