import pandas as pd
import numpy as np
from typing import Sequence, Type
from statsforecast import StatsForecast
from statsforecast.models import _TS


from metaml.meta_models.forecasters.meta_forecaster import MetaForecaster
from metaml.meta_models.forecasters.time_frame import TimeFrame


class LibNixtlaForecaster(MetaForecaster):
    model_class: Type[_TS]

    def _fit(self, observed_data: TimeFrame) -> None:
        # Extract the unique step sizes from the observed data
        unique_step_sizes = list(set(observed_data.step_sizes.values()))

        # Check if there's more than one unique step size
        if len(unique_step_sizes) != 1:
            raise ValueError(
                "At present we can only train Nixtla forecasters on time series which share the same step size."
            )

        if len(self.observed_data.identifier_cols) != 1:
            raise ValueError("At present we only support a single identifier column with Nixtla forecasters.")

        self.model = StatsForecast(
            models=[self.model_class(**self.params.internal_representation)], freq=unique_step_sizes[0]
        )

        self.model.fit(df=self._prepare_observations_for_fit(observed_data=observed_data).dropna())

    def _prepare_observations_for_fit(self, observed_data: TimeFrame) -> pd.DataFrame:
        id_col = observed_data.identifier_cols[0]
        index_col = observed_data.index_col

        observed_data_df = observed_data.data[[id_col, index_col, self.target_name] + self.future_covariate_names]

        return observed_data_df.rename(columns={id_col: "unique_id", index_col: "ds", self.target_name: "y"})

    def _predict(self, n: int, inference_data: TimeFrame) -> TimeFrame:
        if self.future_covariate_names:
            X_df = self._prepare_future_covariates_df(
                inference_data=inference_data, forecast_horizon_relative=np.arange(1, n + 1)
            )
        else:
            X_df = None
        predictions = self.model.predict(
            h=n,
            X_df=X_df,
        )
        predictions = predictions.set_index("ds", append=True)
        predictions.columns = [self.target_name]
        predictions.index = predictions.index.set_names(
            {"unique_id": self.observed_data.identifier_cols[0], "ds": self.observed_data.index_col}
        )
        return TimeFrame(
            data=predictions.reset_index(),
            index_col=self.observed_data.index_col,
            identifier_cols=self.observed_data.identifier_cols,
            step_sizes=self.observed_data.step_sizes,
        )

    def _prepare_future_covariates_df(
        self, inference_data: TimeFrame, forecast_horizon_relative: Sequence[int]
    ) -> pd.DataFrame:
        """Extract future covariates from the inference data.

        Args:
            inference_data (TimeFrame): A TimeFrame object containing the exogenous variables.
            forecast_horizon_relative (Sequence[int]): The sequence of forecasting steps ahead.

        Returns:
            pd.DataFrame: DataFrame of future covariates.
        """

        # Compute time index
        time_index = self.get_forecast_horizon_absolute(forecast_horizon_relative=forecast_horizon_relative)
        series_id = self.observed_data.series_ids[0]

        id_col = self.observed_data.identifier_cols[0]
        index_col = self.observed_data.index_col
        col_name_mapping = {id_col: "unique_id", index_col: "ds"}

        # Get slice of inference data and select only future covariate columns
        return (
            inference_data.get_slice_by_time(series_ids=series_id, start=time_index[0], stop=time_index[-1])[
                self.future_covariate_names
            ]
            .data[[id_col, index_col] + self.future_covariate_names]
            .rename(columns=col_name_mapping)
        )

    def _update(self) -> None:
        self._fit(self.observed_data)
