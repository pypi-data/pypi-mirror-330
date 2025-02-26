from typing import Optional
from enum import Enum
from metaml.meta_models.parameters import (
    ParametersModel,
    OverridableParametersModel,
)


class LoggingLevel(str, Enum):
    SILENT = "Silent"
    VERBOSE = "Verbose"
    INFO = "Info"
    DEBUG = "Debug"


class FeatureBorderType(str, Enum):
    Median = "Median"
    Uniform = "Uniform"
    UniformAndQuantiles = "UniformAndQuantiles"
    MaxLogSum = "MaxLogSum"
    MinEntropy = "MinEntropy"
    GreedyLogSum = "GreedyLogSum"


class OdType(str, Enum):
    Iter = "Iter"
    IncToDec = "IncToDec"


class NanMode(str, Enum):
    Min = "Min"
    Max = "Max"
    Forbidden = "Forbidden"


class FinalCtrComputationMode(str, Enum):
    Default = "Default"
    Skip = "Skip"


class ClassWeights(str, Enum):
    BALANCED = "Balanced"
    SQRT_BALANCED = "SqrtBalanced"


class OverridableParams(OverridableParametersModel):
    # number of threads to use during training, None = use all available we
    # sometimes need to override when setting cpu limits in docker deployments,
    # as os.cpu_count() > docker cpu limit
    thread_count: Optional[int] = None


class Params(ParametersModel):
    _overridable = OverridableParams

    logging_level: LoggingLevel = LoggingLevel.SILENT
    iterations: int = 500
    learning_rate: Optional[float] = None
    depth: int = 6
    l2_leaf_reg: float = 3.0
    model_size_reg: Optional[float] = None
    rsm: Optional[float] = None
    feature_border_type: FeatureBorderType = FeatureBorderType.GreedyLogSum
    fold_permutation_block: int = 1
    od_wait: Optional[int] = None
    od_type: OdType = OdType.IncToDec
    nan_mode: NanMode = NanMode.Min
    max_ctr_complexity: int = 4
    has_time: bool = False
    allow_const_label: bool = False
    random_strength: float = 1.0
    bagging_temperature: float = 1.0
    fold_len_multiplier: Optional[float] = None
    final_ctr_computation_mode: FinalCtrComputationMode = FinalCtrComputationMode.Default
    auto_class_weights: Optional[ClassWeights] = None
    thread_count: Optional[int] = None
