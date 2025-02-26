from pydantic import Extra
from enum import Enum
from typing import Union


from metaml.meta_models.parameters import (
    ParametersModel,
    OverridableParametersModel,
)


class Device(str, Enum):
    CPU = "cpu"
    GPU = "gpu"


class HuggingFaceModelName(str, Enum):
    ROBERTA = "roberta-base"
    BERT = "bert-base-uncased"
    DISTILBERT = "distilbert-base-uncased"
    ALBERT = "albert-base-v2"
    BART = "facebook/bart-base"
    GPT2 = "gpt2"
    ELECTRA = "google/electra-base-discriminator"
    PERCEIVER = "deepmind/language-perceiver"
    TINY_RANDOM_BART = "Narsil/tiny-random-bart"


HugsModelName = str


class ReportTo(str, Enum):
    NONE = "none"
    MLFLOW = "mlflow"


class SchedulerType(Enum):
    LINEAR = "linear"
    COSINE = "cosine"
    COSINE_WITH_RESTARTS = "cosine_with_restarts"
    POLYNOMIAL = "polynomial"
    CONSTANT = "constant"
    CONSTANT_WITH_WARMUP = "constant_with_warmup"


class OverridableParams(OverridableParametersModel):
    device: Device = Device.GPU  # Device to use for training. Either "cpu" or "gpu".


class Params(ParametersModel):
    _overridable = OverridableParams

    batch_size: int = 32
    device: Device
    epochs: int = 2
    learning_rate: float = 5e-5
    lr_scheduler_type: SchedulerType = SchedulerType.LINEAR
    max_length: int = 64
    model: Union[HuggingFaceModelName, HugsModelName] = HuggingFaceModelName.TINY_RANDOM_BART
    report_to: ReportTo = ReportTo.NONE
    warmup_ratio: float = 0.0
