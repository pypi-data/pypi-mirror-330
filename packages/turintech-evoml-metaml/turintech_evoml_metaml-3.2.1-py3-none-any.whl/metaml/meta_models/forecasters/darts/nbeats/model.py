from __future__ import annotations
import joblib
from darts import TimeSeries
from darts.models import NBEATSModel
from typing import List, Union, Optional
from pathlib import Path
from copy import deepcopy


from metaml.exceptions import IOException
from ..darts_forecaster import LibDartsForecaster
from .metadata import metadata
from .parameters import Params


class MetaNBEATSForecaster(LibDartsForecaster):
    """
    This class is a wrapper for the NBEATSModel from Darts, providing fitting and prediction methods for multiple
    time series data.
    """

    metadata = metadata

    def __init__(self, **kwargs):
        """
        Initialize the MetaNBEATSForecaster instance.

        Args:
            **kwargs: Parameters to initialize the NBEATSModel.
        """
        self.params = Params(**kwargs)
        self.model = NBEATSModel(
            **self.params.internal_representation, pl_trainer_kwargs={"devices": 1, "accelerator": "cpu"}
        )

    def _fit_model(
        self,
        target_series: TimeSeries,
        past_covariates: Optional[TimeSeries] = None,
        future_covariates: Optional[TimeSeries] = None,
    ) -> None:
        """
        Fits the N-BEATS model. This model supports past
        covariates but not future covariates.

        """
        # Fit the model. Note that N-BEATS model does not support future covariates.
        self.model.fit(target_series, past_covariates=past_covariates)

    def _model_predict(
        self,
        n: int,
        target_series: TimeSeries,
        past_covariates: Optional[TimeSeries],
        future_covariates: Optional[TimeSeries],
    ) -> List[TimeSeries]:
        # N-BEATS model does not support future covariates so they are not used here.
        return self.model.predict(n, series=target_series, past_covariates=past_covariates)

    def save(self, dirpath: Union[str, Path]) -> Path:
        """Save the model to disk. By default this will use joblib, but we expect this method to be overwritten when
        model specific saving methods are needed, e.g. for the NLPSequenceClassifier. The saved file will be called
        "model.joblib".

        Args:
            dirpath (Union[str, Path]): The path to the directory where "model.joblib" will be saved.

        Returns:
            Path: The path to the saved model.

        """
        dirpath = Path(dirpath)

        # Check if the directory exists
        if not dirpath.is_dir():
            raise IOException(f'The directory "{dirpath}" does not exist.')

        # Create the filepath
        metamodel_path = dirpath / "metamodel.joblib"

        # Save the MetaModel
        joblib.dump(self, metamodel_path)

        model_path = str(dirpath / "model.joblib")
        self.model.save(model_path)

        return dirpath

    @classmethod
    def load(cls, dirpath: Union[str, Path]) -> MetaNBEATSForecaster:
        """Load the model from disk. By default this will use joblib, but we expect this method to be overwritten when
        model specific loading methods are needed, e.g. for the NLPSequenceClassifier. The model is expected to be
        called "model.joblib".

        Args:
            dirpath (Union[str, Path]): The path to directory in which the "model.joblib" artifact will be found.

        Returns:
            MetaModel: The loaded model.

        """
        directory_path: Path = Path(dirpath)
        if not directory_path.is_dir():
            raise IOException(f'The directory "{directory_path}" does not exist.')

        metamodel_path: Path = directory_path / "metamodel.joblib"
        if not metamodel_path.is_file():
            raise IOException(f'The file "{metamodel_path}" does not exist.')

        model_path: Path = directory_path / "model.joblib"
        if not model_path.is_file():
            raise IOException(f'The file "{model_path}" does not exist.')

        metamodel = joblib.load(metamodel_path)
        metamodel.model = NBEATSModel.load(str(model_path))

        return metamodel

    def __deepcopy__(self, memo) -> MetaNBEATSForecaster:
        """Create a deepcopy of the MetaNBEATSForecaster. This custom method is required in order to retain a copy of
        the trainer object, which is otherwise omitted."""
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == "model":
                setattr(result, k, deepcopy(v, memo))
                result.model.trainer = deepcopy(self.model.trainer, memo)  # Manually deepcopy the trainer object
            else:
                setattr(result, k, deepcopy(v, memo))
        return result
