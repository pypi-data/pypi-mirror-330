import pandas as pd
import logging


from typing import Dict, Any
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from mrmr import mrmr_classif
from umap import UMAP


from ..stacking_classifier import LibStackingClassifier, stacking_options
from ..utils import (
    FeatureSetReducer,
    BaseSetReducer,
    RelevanceMetricClassification,
    calculate_number_features,
    f1_score_mrmr,
)
from .metadata import metadata
from .parameters import Params


logger = logging.getLogger("metaml")


class MetaFeatureSetReductionStackingClassifier(LibStackingClassifier):
    """
    This is a Feature Set Reduction Stacking Model class
    derived from Base Stacking class.

    Current implementations to reduce feature space:
    1. Principal Component Analysis (pca)
    2. Uniform Manifold Approximation and Projection for Dimension Reduction (umap)
    3. K-Means clustering (kmeans)

    It can be combined with mrmr filtering of base models predictions.
    """

    metadata = metadata
    params: Params

    def __init__(self, **kwargs) -> None:
        self.params = Params(**kwargs)
        super().__init__()

        # Feature reducer validation
        if not self.params.feature_reducers.issubset(FeatureSetReducer):
            logger.error(f"Not valid feature set reducer: {self.params.feature_reducers}.")
            raise ValueError(f"Not valid feature set reducer: {self.params.feature_reducers}.")
        self.feature_reducers = self.params.feature_reducers

        # Base reducer validation
        if self.params.base_reducer is not None and self.params.base_reducer not in list(BaseSetReducer):
            logger.error(f"Not valid base set reducer: {self.params.base_reducer}.")
            raise ValueError(f"Not valid base set reducer: {self.params.base_reducer}.")
        self.base_reducer = self.params.base_reducer

        # Validate relevance metric
        if self.params.relevance_metric not in list(RelevanceMetricClassification):
            logger.error(f"Not valid relevance metric: {self.params.relevance_metric}.")
            raise ValueError(f"Not valid relevance metric: {self.params.relevance_metric}.")
        self.relevance_metric = self.params.relevance_metric

        # Validate Number of dimensions
        if self.params.number_dimensions <= 0:
            logger.error(f"Not valid number of dimensions: {self.params.number_dimensions}.")
            raise ValueError(f"Not valid number of dimensions: {self.params.number_dimensions}.")
        self.number_dimensions = self.params.number_dimensions

        # Will save the reducer objects in fit
        self.feature_reducer_objects: Dict[str, Any] = {}

    def _stack_fit_transform(self, X: pd.DataFrame, X_base: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        # Reduce base models' predictions (if selected)
        if self.base_reducer == BaseSetReducer.mrmr:
            if self.relevance_metric == RelevanceMetricClassification.f1:
                relevance = f1_score_mrmr
            else:
                relevance = self.relevance_metric
            mrmr = mrmr_classif(
                X=X_base,
                y=y,
                K=calculate_number_features(X_base.shape[1]),
                return_scores=True,
                relevance=relevance,
                show_progress=False,
            )
            self.selected_base_models = mrmr[0]

        X_base_reduced = X_base[self.selected_base_models]

        # Get reduced feature set
        X_train_embedding = self._embed_reduce_fit_transform(X, y)

        # Stack base model predictions and reduced feature set
        X_stack = pd.concat([X_train_embedding, X_base_reduced], axis=1)

        return X_stack

    def _pca_reducer(self, X_: pd.DataFrame) -> None:
        """Creates and fits a PCA object on X_. Adds the object in
        feature_reducer_objects.

        Args:
            X_: training data.

        """
        pca_reducer = PCA(
            n_components=self.number_dimensions,
            random_state=stacking_options.random_state,
        )
        pca_reducer.fit(X_)
        self.feature_reducer_objects["pca"] = pca_reducer

    def _umap_reducer(self, X_: pd.DataFrame) -> None:
        """Creates and fits a  UMAP object on X_. Adds the object in
        feature_reducer_objects.

        Args:
            X_: training data.

        """
        umap_reducer = UMAP(
            n_components=self.number_dimensions,
            random_state=stacking_options.random_state,
        )
        umap_reducer.fit(X_)
        self.feature_reducer_objects["umap"] = umap_reducer

    def _kmeans_reducer(self, X_: pd.DataFrame, y: pd.Series) -> None:
        """Creates and fits a  KMeans object on X_ and y. Adds the object in
        feature_reducer_objects.

        Args:
            X_: training data.
            y: target vector relevant to X_..

        """
        kmeans_reducer = KMeans(
            n_clusters=y.nunique(),
            random_state=stacking_options.random_state,
        )
        kmeans_reducer = kmeans_reducer.fit(X_)
        self.feature_reducer_objects["kmeans"] = kmeans_reducer

    def _kmeans_reducer_distance(self, X_: pd.DataFrame, y: pd.Series) -> None:
        """Creates and fits a  KMeans object on X_ and y. Adds the object in
        feature_reducer_objects.

        Args:
            X_: training data.
            y: target vector relevant to X_.

        """
        kmeans_reducer = KMeans(
            n_clusters=y.nunique(),
            random_state=stacking_options.random_state,
        )
        kmeans_reducer.fit(X_)
        self.feature_reducer_objects["kmeans_distance"] = kmeans_reducer

    def _embed_reduce_fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """Fits feature reducer objects on X and y and transforms them to the
         reduced space.

        Args:
            X: training data.
            y: target vector relevant to X.

        Returns:
            pd.DataFrame: transformed X_ to the reduced space based on the
            selected feature reducer options.

        """
        if FeatureSetReducer.pca in self.feature_reducers:
            self._pca_reducer(X)
        if FeatureSetReducer.umap in self.feature_reducers:
            self._umap_reducer(X)
        if FeatureSetReducer.kmeans in self.feature_reducers:
            self._kmeans_reducer(X, y)
        if FeatureSetReducer.kmeans_distance in self.feature_reducers:
            self._kmeans_reducer_distance(X, y)

        X_embedding = self._embed_reduce_transform(X)
        X_embedding.index = X.index

        return X_embedding

    def _embed_reduce_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforms X to the feature reduced objects based on the fitted
        feature reducer objects.

        Args:
            X: input data.

        Returns:
            pd.DataFrame: transformed X to the reduced space.

        """
        reduced_sets = []
        X_embedding = pd.DataFrame()

        for (
            reducer_name,
            reducer_object,
        ) in self.feature_reducer_objects.items():
            if reducer_name == FeatureSetReducer.kmeans:
                tmp = reducer_object.predict(X)
            else:
                tmp = reducer_object.transform(X)
            tmp_df = pd.DataFrame(tmp)
            tmp_df.columns = [reducer_name + str(i) for i in tmp_df.columns]
            reduced_sets.append(tmp_df)

        if len(reduced_sets) > 0:
            X_embedding = pd.concat(reduced_sets, axis=1)
            X_embedding.index = X.index

        return X_embedding

    def _stack_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_embedding = self._embed_reduce_transform(X)
        df_predictions = self._get_base_predictions(X)
        X_stack = pd.concat([X_embedding, df_predictions], axis=1)
        return X_stack
