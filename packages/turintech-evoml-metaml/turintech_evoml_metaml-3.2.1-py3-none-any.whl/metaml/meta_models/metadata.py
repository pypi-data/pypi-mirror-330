from pydantic import BaseModel, Field
from typing import Set, List
from enum import Enum


from metaml.meta_models.names import ModelNameType


class ModelTag(str, Enum):
    """All available model tags."""

    classifier = "classifier"
    regressor = "regressor"
    forecaster = "forecaster"
    ts = "ts"
    experimental = "experimental"
    nlp = "nlp"
    custom_io = "custom_io"


class ModelTypeEnum(str, Enum):
    """All available model types."""

    tree = "Tree-Based Model"
    ensemble = "Ensemble Model"
    linear = "Linear Model"
    gradient = "Gradient Model"
    forecasting = "Forecasting Model"
    bayesian = "Bayesian Model"
    kernel = "Kernel Model"
    semisupervised = "Semi-Supervised Model"
    support_vector_machine = "Support Vector Machine Model"
    deep_learning = "Deep Learning Model"
    nearest_neighbours = "Nearest Neighbours Model"
    baseline = "Baseline Model"
    statistical = "Statistical Model"


class Supports(BaseModel):
    probabilities: bool  # Supports the predict_proba method
    feature_importances: bool = Field(..., alias="featureImportances")  # Provides feature importances

    class Config:
        allow_population_by_field_name = True


class MetaData(BaseModel):
    """Metadata of a model which can be imported without having to import the model and its dependencies."""

    # Fields to be used for filtering
    model_name: ModelNameType = Field(..., alias="model")
    model_type: Set[ModelTypeEnum] = Field(..., alias="modelType")
    tags: Set[ModelTag]

    # UI fields
    description: str = Field(..., alias="modelDescription")
    advantages: List[str]
    disadvantages: List[str]
    prime: List[str]  # The most important parameters for display on the front end
    display_name: str = Field(..., alias="displayName")

    # Flags of model capabilities
    supports: Supports

    class Config:
        allow_population_by_field_name = True

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = kwargs.get("by_alias", True)  # Use aliases by default
        return super().dict(*args, **kwargs)

    def json(self, *args, **kwargs):
        kwargs["by_alias"] = kwargs.get("by_alias", True)  # Use aliases by default
        return super().json(*args, **kwargs)
