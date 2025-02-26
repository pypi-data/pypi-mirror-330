import importlib
import json
import inspect
from pydantic import BaseModel
from typing import Callable, Dict, Final, Union, Any, List, Type
from pathlib import Path


import metaml
from metaml.factory.constraint_handling.combine_constrained_parameters import (
    combine_constrained_parameters,
)
from metaml.exceptions import ParseKwargsException
from metaml.factory.parameter_settings import ParamSettings, InputParameter
from metaml.meta_models.metadata import MetaData, ModelTag
from metaml.parameter_space.graph import ParameterGraph, ParameterGraphModel
from metaml.meta_models.meta_model import MetaModel
from metaml.meta_models.classifiers.meta_classifier import MetaClassifier
from metaml.meta_models.regressors.meta_regressor import MetaRegressor
from metaml.meta_models.forecasters.meta_forecaster import MetaForecaster
from metaml.meta_models.names import (
    ModelNameType,
    ClassifierName,
    ForecasterName,
    RegressorName,
)
from metaml._util.utils import is_number


ModelPath = str
"""A string representing a path to the package containing a model. The path is a dot-separated string relative to the
metaml.meta_models package. For example, the path to the `RandomForestClassifier` model is 
`classifiers.sklearn.random_forest`."""


model_paths: List[ModelPath] = [
    # ------------------------------------------------------------------------------------------------------------------
    # Regressors
    # ------------------------------------------------------------------------------------------------------------------
    # Scikit-learn
    "regressors.sklearn.ard",
    "regressors.sklearn.bayesian_ridge",
    "regressors.sklearn.decision_tree",
    "regressors.sklearn.elastic_net",
    "regressors.sklearn.gradient_boosting",
    "regressors.sklearn.hist_gradient_boosting",
    "regressors.sklearn.huber",
    "regressors.sklearn.lasso",
    "regressors.sklearn.linear",
    "regressors.sklearn.linear_svr",
    "regressors.sklearn.mean_dummy",
    "regressors.sklearn.median_dummy",
    "regressors.sklearn.passive_aggressive",
    "regressors.sklearn.random_forest",
    "regressors.sklearn.ridge",
    "regressors.sklearn.sgd",
    "regressors.sklearn.svr",
    # HuggingFace
    "regressors.huggingface.nlp_sequence",
    # Intelex
    "regressors.intelex.elastic_net",
    "regressors.intelex.linear",
    "regressors.intelex.random_forest",
    "regressors.intelex.svr",
    # Stacking
    "regressors.stacking.feature_set_reduction",
    "regressors.stacking.generic",
    "regressors.stacking.base_set_reduction",
    # LightGBM
    "regressors.lightgbm.lgbm",
    # Lightning
    "regressors.lightning.fista",
    "regressors.lightning.cd",
    # CatBoost
    "regressors.catboost.catboost",
    # XGBoost
    "regressors.xgboost.xgb",
    # ------------------------------------------------------------------------------------------------------------------
    # Forecasters
    # ------------------------------------------------------------------------------------------------------------------
    # Darts
    "forecasters.darts.linear_regression",
    "forecasters.darts.nbeats",
    # Nixtla
    "forecasters.nixtla.arima",
    "forecasters.nixtla.auto_arima",
    "forecasters.nixtla.auto_ces",
    "forecasters.nixtla.auto_ets",
    "forecasters.nixtla.auto_theta",
    "forecasters.nixtla.garch",
    "forecasters.nixtla.historic_average",
    "forecasters.nixtla.random_walk_with_drift",
    "forecasters.nixtla.seasonal_naive",
    "forecasters.nixtla.seasonal_window_average",
    # Sktime
    "forecasters.sktime.naive_last",
    "forecasters.sktime.auto_ets",
    "forecasters.sktime.naive_drift",
    "forecasters.sktime.auto_arima",
    "forecasters.sktime.naive_mean",
    "forecasters.sktime.arima",
    # ------------------------------------------------------------------------------------------------------------------
    # Classifiers
    # ------------------------------------------------------------------------------------------------------------------
    # Scikit-learn
    "classifiers.sklearn.random_forest",
    "classifiers.sklearn.perceptron",
    "classifiers.sklearn.hist_gradient_boosting",
    "classifiers.sklearn.gaussian_naive_bayes",
    "classifiers.sklearn.decision_tree",
    "classifiers.sklearn.prior_dummy",
    "classifiers.sklearn.extra_trees",
    "classifiers.sklearn.gaussian_process",
    "classifiers.sklearn.gradient_boosting",
    "classifiers.sklearn.uniform_dummy",
    "classifiers.sklearn.nearest_centroid",
    "classifiers.sklearn.linearsvc",
    "classifiers.sklearn.svc",
    "classifiers.sklearn.logistic_regression",
    "classifiers.sklearn.sgd",
    "classifiers.sklearn.passive_aggressive",
    "classifiers.sklearn.stratified_dummy",
    "classifiers.sklearn.quadratic_discriminant_analysis",
    "classifiers.sklearn.linear_discriminant_analysis",
    # HuggingFace
    "classifiers.huggingface.nlp_sequence",
    # Intelex
    "classifiers.intelex.logistic_regression",
    "classifiers.intelex.random_forest",
    "classifiers.intelex.svc",
    # Stacking
    "classifiers.stacking.feature_set_reduction",
    "classifiers.stacking.generic",
    "classifiers.stacking.base_set_reduction",
    # LightGBM
    "classifiers.lightgbm.lgbm",
    # Lightning
    "classifiers.lightning.fista",
    "classifiers.lightning.cd",
    "classifiers.lightning.svrg",
    "classifiers.lightning.saga",
    "classifiers.lightning.sdca",
    "classifiers.lightning.adagrad",
    # CatBoost
    "classifiers.catboost.catboost",
    # XGBoost
    "classifiers.xgboost.xgb",
]


Importer = Callable[[], Union[Type[MetaClassifier], Type[MetaRegressor], Type[MetaForecaster]]]
"""A callable that returns the class defining a model. This allows us to delay importing dependencies until required."""


class ModelEntry(BaseModel):
    metadata: MetaData
    parameter_graph: ParameterGraph
    importer: Importer
    parameter_settings: ParamSettings

    class Config:
        arbitrary_types_allowed = True


class Factory:
    split: Final[str] = "~~~"
    registry: Dict[ModelNameType, ModelEntry]

    # Construction methods
    def __init__(self, model_paths: List[ModelPath]):
        self.registry = {}
        self._register_models(model_paths)

    def _register_models(self, model_paths: List[ModelPath]):
        """Register all models in the model_list."""
        for model_path in model_paths:
            metadata = self._load_metadata(model_path)
            param_graph: ParameterGraph = self._load_parameter_graph(model_path)
            importer = self._load_importer(model_path)
            parameter_settings = self._construct_param_settings(metadata, param_graph.export())

            if metadata.model_name in self.registry:
                raise KeyError(f"A model named {metadata.model_name} already exists in the register")

            # Use model_name in the metadata as the key in the register
            self.registry[metadata.model_name] = ModelEntry(
                metadata=metadata,
                parameter_graph=param_graph,
                importer=importer,
                parameter_settings=parameter_settings,
            )

    @staticmethod
    def _load_metadata(model_path: ModelPath) -> MetaData:
        """Load the metadata of the desired model."""
        metadata_module = importlib.import_module(f"metaml.meta_models.{model_path}.metadata")
        return metadata_module.metadata  # Use metadata instance directly

    @staticmethod
    def _load_parameter_graph(model_path: ModelPath) -> ParameterGraph:
        """Load the parameter graph of the desired model."""
        graph_module = importlib.import_module(f"metaml.meta_models.{model_path}.space.graph")
        return graph_module.parameter_graph  # Use parameter_graph instance directly

    @staticmethod
    def _load_importer(
        model_path: str,
    ) -> Importer:  # Adjust the type annotation for model_path as needed
        """Load the importer of the desired model."""

        def import_model() -> Union[Type[MetaClassifier], Type[MetaRegressor], Type[MetaForecaster]]:
            """
            Finds and imports a subclass of MetaModel in a module specified by model_path.
            Only includes subclasses defined within the specified module.

            Returns:
                type: The subclass type if found.

            Raises:
                ImportError: If the module could not be imported.
                ValueError: If multiple subclasses are found.
            """
            module_name = f"metaml.meta_models.{model_path}.model"
            base_class = MetaModel

            subclasses = []

            try:
                module = importlib.import_module(module_name)
            except ImportError as e:
                raise ImportError(f"Could not import module {module_name}") from e

            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, base_class)
                    and obj != base_class
                    and obj.__module__ == module_name
                ):
                    subclasses.append(obj)

            if len(subclasses) > 1:
                raise ValueError(
                    "Multiple subclasses found. Please make sure only one subclass is defined in the module."
                )

            return subclasses[0]

        return import_model

    @staticmethod
    def _construct_param_settings(metadata: MetaData, parameter_graph_model: ParameterGraphModel) -> ParamSettings:
        """Construct the parameter settings of the desired model by merging the metadata, the input parameters and any
        constraint information present in the json config, if present."""
        json_contents = None
        for param_file in (
            Path(metaml.meta_models.__file__).parent.resolve().glob(f"**/{metadata.model_name.value}.json")
        ):
            with open(param_file, "r") as file:
                json_contents = json.load(file)
        if not json_contents:
            raise IOError(f"File not found: {metadata.model_name.value}.json.")
        param_settings = {}
        if "constraintParameters" in json_contents:
            param_settings["constraintParameters"] = json_contents["constraintParameters"]
        param_settings["parameters"] = parameter_graph_model.parameters
        param_settings["constraints"] = parameter_graph_model.constraints
        param_settings["metadata"] = metadata
        param_settings["inputParameters"] = parameter_graph_model.input_parameters  # Deprecated
        return ParamSettings(**param_settings)

    # Getters to obtain information about the models
    def get_entry(self, model_name: ModelNameType) -> ModelEntry:
        """Get all information about the desired model."""
        return self.registry[model_name]

    def get_metadata(self, model_name: ModelNameType) -> MetaData:
        """Get the metadata of the desired model."""
        return self.registry[model_name].metadata

    def get_parameter_graph(self, model_name: ModelNameType) -> ParameterGraph:
        """Get the parameter graph of the desired model."""
        return self.registry[model_name].parameter_graph

    def get_model_class(
        self, model_name: ModelNameType
    ) -> Union[Type[MetaClassifier], Type[MetaRegressor], Type[MetaForecaster]]:
        """Get the class of the desired model."""
        return self.registry[model_name].importer()

    def get_model(self, model_name: ModelNameType, **kwargs) -> Union[MetaClassifier, MetaForecaster, MetaRegressor]:
        """Obtain an instance of the desired model.

        Args:
            model_name: Name of the desired model.
            **kwargs: The parameters which will be passed to the model when it is constructed.

        Returns:
            The desired model.

        """
        input_params = kwargs
        kwargs = self._parse_kwargs(**kwargs)  # splits complex parameters into simple ones
        model_class = self.get_model_class(model_name)
        model = model_class(**kwargs)
        model.set_input_params(input_params)
        return model

    def _parse_kwargs(self, **kwargs) -> Dict[str, Any]:
        """Splits compound keyword arguments (e.g. {"a~~b": "1~~~2"} -> {"a": 1, "b": 2} and returns a dictionary
        mapping simple keyword arguments to their values."""
        if self.split not in str(kwargs):
            return kwargs
        args = {}
        for key, value in kwargs.items():
            if self.split in key:
                keys = key.split(self.split)
                values = str(value).split(self.split)
                if len(keys) != len(values):
                    err_msg: str = "(MetaML) The dependent parameters's keys: {} and their values: {} are not matched."
                    raise ParseKwargsException(err_msg.format(keys, values))
                for split_key, split_value in zip(keys, values):
                    if split_value == "True":
                        args[split_key] = True
                    elif split_value == "False":
                        args[split_key] = False
                    elif split_value == "None" or split_value.lower() == "null":
                        args[split_key] = None
                    elif is_number(split_value):
                        number = float(split_value)
                        args[split_key] = int(number) if number.is_integer() else number
                    else:
                        args[split_key] = split_value
            else:
                args[key] = value
        return args

    def get_simple_param_by_name(self, model_name: ModelNameType) -> ParamSettings:
        """Get the parameter settings for a model by its name without combining constrained parameters.

        Args:
            model_name (ModelNameType): The name of the model.

        Returns:
            ParamSettings: The parameter settings for the model.
        """

        return self.registry[model_name].parameter_settings

    def get_param_by_name(self, model_name: ModelNameType) -> ParamSettings:
        """Get the parameter settings for a model by its name. Parameters which share a constraint relationship will
        be combined into a single unconstrained parameter.

        Args:
            model_name (ModelNameType): The name of the model.

        Returns:
            ParamSettings: The parameter settings for the model.
        """
        return combine_constrained_parameters(self.get_simple_param_by_name(model_name))

    def get_model_list(
        self,
        contains: Union[List[ModelTag], ModelTag, None] = None,
        excludes: Union[List[ModelTag], ModelTag, None] = None,
    ) -> List[ModelNameType]:
        """Get a list of models which possess the desired tags.

        Args:
            contains (Optional[Union[List[ModelTag], ModelTag]]): List of desired tags.
            excludes (Optional[Union[List[ModelTag], ModelTag]]): List of undesired tags.

        Returns:
            List[ModelNameType]: List of models which have the tags in contains and do not have the tags in excludes.

        """
        if excludes is None:
            excludes = []
        if contains is None:
            contains = []
        contains_set = {contains} if isinstance(contains, str) else set(contains)
        excludes_set = {excludes} if isinstance(excludes, str) else set(excludes)
        return [
            model_name
            for model_name, entry in self.registry.items()
            if contains_set.intersection(entry.metadata.tags) == contains_set
            and excludes_set.intersection(entry.metadata.tags) == set([])
        ]

    def get_classifiers(self) -> List[ClassifierName]:
        """Provides a list of all classifiers."""
        return self.get_model_list(contains=ModelTag.classifier, excludes=ModelTag.experimental)

    def get_regressors(self) -> List[RegressorName]:
        """Provides a list of all regressors."""
        return self.get_model_list(contains=ModelTag.regressor, excludes=ModelTag.experimental)

    def get_forecasters(self) -> List[ForecasterName]:
        """Provides a list of all forecasters."""
        return self.get_model_list(contains=ModelTag.forecaster, excludes=ModelTag.experimental)

    # Load saved models
    def load(self, dirpath: Union[str, Path], model_name: ModelNameType) -> MetaModel:
        """Load a model from disk using the model specific implementation of the load method."""
        return self.get_model_class(model_name).load(dirpath=dirpath)


# Instantiate the factory to be used by the rest of the library.
factory = Factory(model_paths)
