from typing import Optional
from enum import Enum


from metaml.meta_models.parameters import ParametersModel


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


class CounterCalcMethod(str, Enum):
    Full = "Full"
    SkipTest = "SkipTest"


class FinalCtrComputationMode(str, Enum):
    Default = "Default"
    Skip = "Skip"


class ScoreFunction(str, Enum):
    COSINE = "Cosine"
    L2 = "L2"


class LeafEstimationBacktracking(str, Enum):
    NO = "No"
    ANY_IMPROVEMENT = "AnyImprovement"


class BoostingType(str, Enum):
    ORDERED = "Ordered"
    PLAIN = "Plain"


class BootstrapType(str, Enum):
    BAYESIAN = "Bayesian"
    BERNOULLI = "Bernoulli"
    MVS = "MVS"


class Params(ParametersModel):
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
    counter_calc_method: Optional[CounterCalcMethod] = None
    max_ctr_complexity: int = 4
    has_time: bool = False
    allow_const_label: bool = False
    random_strength: float = 1.0
    fold_len_multiplier: Optional[float] = None
    final_ctr_computation_mode: FinalCtrComputationMode = FinalCtrComputationMode.Default
    score_function: ScoreFunction = ScoreFunction.COSINE
    leaf_estimation_backtracking: LeafEstimationBacktracking = LeafEstimationBacktracking.ANY_IMPROVEMENT
    model_shrink_rate: Optional[float] = None
    boost_from_average: bool = False
    boosting_type: Optional[BoostingType] = None
    approx_on_full_history: bool = False
    bagging_temperature: Optional[float] = None
    bootstrap_type: BootstrapType = BootstrapType.MVS
    subsample: Optional[float] = None
