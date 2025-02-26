from pydantic import Extra
from enum import Enum


from metaml.meta_models.parameters import (
    ParametersModel,
    OverridableParametersModel,
)


class Device(str, Enum):
    CPU = "cpu"
    GPU = "gpu"


class HuggingFaceModelName(str, Enum):
    ROBERTA_BASE = "roberta-base"
    BERT_BASE_CASED = "bert-base-cased"
    BERT_BASE_UNCASED = "bert-base-uncased"
    DISTILBERT_BASE_CASED = "distilbert-base-cased"
    DISTILBERT_BASE_UNCASED = "distilbert-base-uncased"
    ALBERT_BASE_V2 = "albert-base-v2"
    DYNAMIC_TINY_BERT = "Intel/dynamic_tinybert"


class OverridableParams(OverridableParametersModel):
    device: Device = Device.GPU  # Device to use for training. Either "cpu" or "gpu".


class Params(ParametersModel):
    _overridable = OverridableParams

    model: HuggingFaceModelName = HuggingFaceModelName.DYNAMIC_TINY_BERT
    learning_rate: float = 5e-5
    epochs: int = 2
    max_length: int = 64
    device: Device

    class Config:
        extra = Extra.forbid
