from __future__ import annotations
from typing import Union
from pathlib import Path
from abc import abstractmethod

from metaml.meta_models.meta_model import MetaModel
from metaml.meta_models.classifiers.xgboost.xgb.parameters import (
    Params as ClassifierParams,
)
from metaml.meta_models.regressors.xgboost.xgb.parameters import (
    Params as RegressorParams,
)
from metaml.exceptions import IOException
from metaml import ModelTag

PARAMS_FILE_NAME = "params.json"  # Name of the file where the parameters are stored when using `load_from_dir`.


class MetaModelXGBoost(MetaModel):
    """This class provides the load/save functionalities used by xgboost models
    - classification and regression"""

    def save(self, dirpath: Union[str, Path]) -> Path:
        """Save the model to a directory. We will save the
        xgboost model and the parameters used to initialize the model.

        Args:
            dirpath (Union[str, Path]): The directory to which the model will be saved.

        """
        dirpath = Path(dirpath)

        # Check if the directory exists
        if not dirpath.is_dir():
            raise IOException(f'The directory "{dirpath}" does not exist.')

        # Create the filepath
        filepath = dirpath / "model.ubj"

        # Save the model using xgboost specific method
        self.model.save_model(filepath)

        # Save the parameters.
        params_path = dirpath / PARAMS_FILE_NAME
        params_path.write_text(self.params.json())

        self._save(dirpath)

        return dirpath

    @classmethod
    def load(cls, dirpath: Union[str, Path]) -> MetaModelXGBoost:
        """Load the model from a directory. The directory must contain the xgboost model and its parameters. If the
        directory contains the parameters then these will be used to initialize the model, otherwise we will use the
        default parameters."""
        directory_path: Path = Path(dirpath)
        if not directory_path.is_dir():
            raise IOException(f'Directory "{directory_path}" does not exist.')

        # Load the parameters or use the defaults.
        params_path = directory_path / PARAMS_FILE_NAME
        if cls._estimator_type == ModelTag.classifier:
            Params = ClassifierParams
        else:
            Params = RegressorParams

        if params_path.exists():
            params = Params.parse_file(params_path).dict()
        else:
            params = Params().dict()

        # Initialize the model.
        top_level_model: MetaModelXGBoost = cls(**params)

        xgb_model = cls.get_xgboost_model()

        # Extract xgboost model
        filepath = directory_path / "model.ubj"
        if not filepath.is_file():
            raise IOException(f'File "{filepath}" does not exist.')

        xgb_model.load_model(filepath)
        top_level_model.model = xgb_model

        top_level_model = cls._load(directory_path, top_level_model)

        return top_level_model

    @classmethod
    @abstractmethod
    def get_xgboost_model(cls) -> MetaModelXGBoost:
        pass

    def _save(self, dirpath: Union[str, Path]) -> Path:
        """Model specific save logic."""
        pass

    @classmethod
    def _load(cls, dirpath: Union[str, Path], top_level_model: MetaModelXGBoost) -> MetaModelXGBoost:
        """Model specific load logic."""
        return top_level_model
