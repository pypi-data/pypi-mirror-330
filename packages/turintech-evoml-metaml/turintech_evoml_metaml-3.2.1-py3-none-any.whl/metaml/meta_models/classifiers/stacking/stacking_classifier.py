import numpy as np
import pandas as pd
import logging


from abc import abstractmethod
from functools import reduce
from typing import List, Union
from sklearn.model_selection import cross_val_predict
from sklearn.base import clone


from .utils import StackingOptions
from metaml.meta_models.classifiers.meta_classifier import MetaClassifier
from metaml.meta_models.names import ClassifierName
from metaml._util.typing import strict
from metaml.exceptions import PredictProbaException
from metaml.factory import factory
from .parameters import StackingParams


logger = logging.getLogger("metaml")


# Default options
default_stacking_classifiers = [
    factory.get_model(ClassifierName.logistic_regression_classifier),
    factory.get_model(ClassifierName.random_forest_classifier),
]
stacking_options = StackingOptions()
default_stacking_meta_classifier = factory.get_model(ClassifierName.random_forest_classifier)


class LibStackingClassifier(MetaClassifier):
    """
    This is a Base Stacking Model class that provides
    an interface to stacking methods
    """

    params: StackingParams
    classifiers: strict(list, MetaClassifier)
    model: Union[MetaClassifier]

    def __init__(self) -> None:
        """
        Constructor for Base Stacking Model
        """

        self.classifiers = clone(self.params.classifiers)
        self.model = clone(self.params.meta_classifier)

        # Selected base models - may be updated in fit if subclass reduces the
        # space of base models
        self.selected_base_models: List[int] = list(range(len(self.classifiers)))

    @abstractmethod
    def _stack_fit_transform(self, X: pd.DataFrame, X_base: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """Creates a new set of features for use when fitting the metaclassifier.
        These new features are generated from the original features X and the
        predictions of the base models using cross-validation, i.e., X_base =
        [cross_val_predict(model, X, y) for model in base_models].
        Various feature selection techniques and transformations are used to
        perform this task. The procedure varies for each subclass and is
        determined by the implementation of this method.

        Args:
            X: features of the original training dataset.
            X_base: dataset of predictions of base models. It is created using
            cross-validation on X.
            y: target vector relative to X.

        Returns:
            pd.DataFrame: dataset created from X and X_base.

        """
        ...

    def _fit(self, X: pd.DataFrame, y: pd.Series):
        """Responsible for fitting the stacking model, including both the base
        classifiers and the metaclassifier.

        Args:
            X: training dataset.
            y: target vector relative to X.

        Returns:
            Fitted estimator.

        """
        # Clone base models and meta classifier
        self.classifiers = clone(self.classifiers)
        self.model = clone(self.model)

        # Get predictions from base estimators
        cv_pred_ls = [cross_val_predict(model, X, y, cv=stacking_options.cv_) for model in self.classifiers]
        X_base = reduce(
            lambda x, y: pd.concat([pd.DataFrame(x), pd.DataFrame(y)], axis=1),
            cv_pred_ls,
            pd.DataFrame(),
        )
        X_base.columns = list(range(len(self.classifiers)))
        X_base.index = X.index

        # Fit base estimators
        for model in self.classifiers:
            model.fit(X, y)

        X_stack = self._stack_fit_transform(X, X_base, y)
        X_stack.columns = X_stack.columns.astype(str)
        # Fit metaclassifier on X_stack
        self.model.fit(X_stack, y)

    @abstractmethod
    def _stack_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Creates the stacked dataframe that will be used for predict and score
        methods of metaclassifier.

        Args:
            X: input data.

        Returns:
            pd.DataFrame: dataset created from X and predictions of base models
             on X.

        """
        ...

    def _get_base_predictions(self, X: pd.DataFrame) -> pd.DataFrame:
        """Creates a dataframe with the predictions of the selected (possible
        all) base models.

        Args:
            X: input data.

        Returns:
            pd.DataFrame: a dataframe where each column contains the
            predictions of one of the selected base models.

        """
        df = pd.DataFrame()
        for i in self.selected_base_models:
            model = self.classifiers[i]
            pred = model.predict(X)
            df[i] = pred
        df.index = X.index
        return df

    def _predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Responsible for producing predictions on X.

        Args:
            X: input data.

        Returns:
            np.ndarray: predicted target vales for X.

        """
        df_stack = self._stack_transform(X)
        df_stack.columns = df_stack.columns.astype(str)
        return self.model.predict(df_stack)

    def has_predict_proba(self) -> bool:
        """Checks if the stacking model supports a predict_proba method.

        Returns:
            bool: whether the metaclassifier has a predict_proba
             method.

        """
        return bool(hasattr(self.model, "predict_proba"))

    def _predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Obtain probability estimates for the predictions of the stacking
        model.

        Args:
            X: Input data for prediction.

        Returns:
           np.ndarray: probabilities for each class for all data points in X.

        """

        if hasattr(self.model, "predict_proba"):
            df_stack = self._stack_transform(X)
            df_stack.columns = df_stack.columns.astype(str)
            return self.model.predict_proba(df_stack)

        # no predict_proba method
        err_msg = f"The metaclassifier {type(self.model).__name__} doesn't have predict_proba method."
        raise PredictProbaException(err_msg)
