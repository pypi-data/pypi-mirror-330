from darts.models import RegressionModel
from sklearn.linear_model import LinearRegression
from typing import Optional, List, Sequence
from darts import TimeSeries


from ..darts_forecaster import LibDartsForecaster
from .metadata import metadata
from .parameters import Params


class MetaLinearRegressionForecaster(LibDartsForecaster):
    """
    This class is a wrapper for the RegressionModel (with LinearRegression as the underlying model)
    from Darts, providing forecasting for multiple time series.

    It uses past and future covariates if they are available in the training data. The forecasted results are returned
    as a TimeFrame object.

    Attributes:
        metadata: Meta data information for the class.
        model: RegressionModel instance from Darts, initialized when fit() method is called.
        params: An instance of Params class to hold parameters for RegressionModel.
    """

    metadata = metadata
    model: RegressionModel
    params: Params

    def __init__(self, **kwargs):
        """
        Initialize the MetaLinearRegressionForecaster instance.

        Args:
            **kwargs: Parameters to initialize the RegressionModel and the underlying LinearRegression model.
                      Expected parameters are 'fit_intercept', 'lags', 'lags_past_covariates', 'lags_future_covariates',
                      and 'output_chunk_length'.
        """
        self.params = Params(**kwargs)

    def _initialize_model(self) -> None:
        """
        Initialize the RegressionModel with the parameters depending on the dataset.

        If the data does not contain past covariates or future covariates, the respective parameters lags_past_covariates
        and lags_future_covariates are left unset to present an exception when the model is trained.
        """
        self.model = RegressionModel(
            model=LinearRegression(fit_intercept=self.params.fit_intercept),
            lags=self.params.lags,
            lags_past_covariates=self.params.lags_past_covariates if self.past_covariate_names else None,
            lags_future_covariates=(0, self.params.lags_future_covariates) if self.future_covariate_names else None,
            output_chunk_length=self.params.output_chunk_length,
        )

    def _fit_model(
        self,
        target_series: TimeSeries,
        past_covariates: Optional[TimeSeries] = None,
        future_covariates: Optional[TimeSeries] = None,
    ) -> None:
        """
        Fits the Linear Regression model to the given target series and covariates.

        This method first initializes the RegressionModel with the parameters held in self.params. It then fits the model to
        the target series and covariates data.

        Args:
            target_series_list (List[TimeSeries]): List of target series.
            past_covariates_list (Optional[List[TimeSeries]]): List of past covariates series. Defaults to None.
            future_covariates_list (Optional[List[TimeSeries]]): List of future covariates series. Defaults to None.

        Raises:
            ValueError: If the model fails to fit the data.
        """

        # Initialize the model
        self._initialize_model()

        # Fit the model
        self.model.fit(target_series, past_covariates=past_covariates, future_covariates=future_covariates)

    def _model_predict(
        self,
        n: int,
        target_series: TimeSeries,
        past_covariates: Optional[TimeSeries],
        future_covariates: Optional[TimeSeries],
    ) -> List[TimeSeries]:
        return self.model.predict(
            n=n,
            series=target_series,
            past_covariates=past_covariates,
            future_covariates=future_covariates,
        )
