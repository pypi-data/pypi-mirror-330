import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from typing import Iterable, Union
from pathlib import Path


from metaml.meta_models.common.xgboost import MetaModelXGBoost
from metaml.meta_models.classifiers.meta_classifier import MetaClassifier
from metaml._util.utils import convert_nonnumeric_to_category_columns


class LibXGBoostClassifier(MetaClassifier, MetaModelXGBoost):
    encoder: LabelEncoder  # Used to map target labels to consecutive integers

    def _fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model.

        Args:
            X (pd.DataFrame): A dataframe of shape (n_samples, n_features) containing the features of each sample of
            training data.
            y (pd.Series): A series of shape (n_samples,) containing the target labels of the samples in X.

        """
        # Initialize the LabelEncoder
        self.label_encoder = LabelEncoder()

        # Fit the label encoder and transform y to integer labels
        y_encoded = self.label_encoder.fit_transform(y)

        # Store the original classes
        self.classes_ = self.label_encoder.classes_

        # Fit the model with the encoded labels
        self.model.fit(convert_nonnumeric_to_category_columns(X), y_encoded)

    def _predict(self, X: pd.DataFrame) -> Iterable:
        # Predict using the model with encoded features
        encoded_predictions = self.model.predict(convert_nonnumeric_to_category_columns(X))

        # Inverse transform the predictions to get original labels
        original_label_predictions = self.label_encoder.inverse_transform(encoded_predictions)
        return original_label_predictions

    def _predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> Iterable:
        return self.model.predict_proba(convert_nonnumeric_to_category_columns(X))

    @classmethod
    def get_xgboost_model(cls):
        return XGBClassifier()

    def _save(self, dirpath: Union[str, Path]):
        """Model specific logic to save the label encoder."""
        # Ensure dirpath is a Path object
        dirpath = Path(dirpath)

        # Define the file path for saving the LabelEncoder
        encoder_file_path = dirpath / "label_encoder.pkl"

        # Open the file and write the pickled encoder
        with open(encoder_file_path, "wb") as file:
            pickle.dump(self.label_encoder, file)

    @classmethod
    def _load(cls, filepath: Union[str, Path], top_level_model: MetaModelXGBoost) -> MetaModelXGBoost:
        """Model specific logic to load the label encoder."""
        # Ensure filepath is a Path object
        filepath = Path(filepath)

        # Define the file path for loading the LabelEncoder
        encoder_file_path = filepath / "label_encoder.pkl"

        # Open the file and load the pickled encoder
        with open(encoder_file_path, "rb") as file:
            top_level_model.label_encoder = pickle.load(file)

        return top_level_model
