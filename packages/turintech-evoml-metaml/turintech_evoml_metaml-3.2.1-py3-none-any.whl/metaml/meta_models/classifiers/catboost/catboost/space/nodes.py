from metaml.parameter_space.node import (
    CategoricalNode,
    FloatNode,
    IntegerNode,
    MixedNode,
)
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


allow_const_label = CategoricalNode(
    name="allow_const_label",
    label="Allow const label",
    description="Use it to train models with datasets that have equal label values for all objects.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
auto_class_weights = CategoricalNode(
    name="auto_class_weights",
    label="Automatic class weights",
    description="Enables automatic class weights calculation. It may be useful for imbalanced datasets.",
    domain=CategoricalSet(categories={"None", "SqrtBalanced", "Balanced"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
bagging_temperature = FloatNode(
    name="bagging_temperature",
    label="Bagging temperature",
    description="Defines the settings of the Bayesian bootstrap. It is used by default in classification and regression modes.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
depth = IntegerNode(
    name="depth",
    label="Depth",
    description="The depth of the tree.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=True,
    default_value=6,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
feature_border_type = CategoricalNode(
    name="feature_border_type",
    label="Feature border type",
    description="The quantization mode for numerical features.",
    domain=CategoricalSet(
        categories={
            "Median",
            "MinEntropy",
            "GreedyLogSum",
            "Uniform",
            "UniformAndQuantiles",
        }
    ),
    enabled=False,
    default_value="GreedyLogSum",
    constraint=False,
    constraintInformation=None,
)
final_ctr_computation_mode = CategoricalNode(
    name="final_ctr_computation_mode",
    label="Final CTR computation mode",
    description="Final CTR computation mode.",
    domain=CategoricalSet(categories={"Default", "Skip"}),
    enabled=False,
    default_value="Default",
    constraint=False,
    constraintInformation=None,
)
fold_len_multiplier = MixedNode(
    name="fold_len_multiplier",
    label="Fold length multiplier",
    description="Coefficient for changing the length of folds.",
    domain=MixedSet(
        float_set=FloatSet(),
        integer_set=IntegerSet.closedopen(2, 11),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
fold_permutation_block = IntegerNode(
    name="fold_permutation_block",
    label="Fold permutation block",
    description="Objects in the dataset are grouped in blocks before the random permutations. This parameter defines the size of the blocks. The smaller is the value, the slower is the training. Large values may result in quality degradation.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
has_time = CategoricalNode(
    name="has_time",
    label="Has time",
    description="Use the order of objects in the input data (do not perform random permutations during the Transforming categorical features to numerical features and Choosing the tree structure stages).",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
iterations = IntegerNode(
    name="iterations",
    label="Iterations",
    description="The number of iterations.",
    domain=IntegerSet.closedopen(1, 1001),
    enabled=True,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
l2_leaf_reg = FloatNode(
    name="l2_leaf_reg",
    label="L2 regularization coefficient",
    description="Coefficient at the L2 regularization term of the cost function.",
    domain=FloatSet.closed(0.0, 10.0),
    enabled=False,
    default_value=3.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
learning_rate = MixedNode(
    name="learning_rate",
    label="Learning rate",
    description="Step size shrinkage used in update to prevents overfitting. After each boosting step, we can directly get the weights of new features, and eta shrinks the feature weights to make the boosting process more conservative.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0001, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
max_ctr_complexity = IntegerNode(
    name="max_ctr_complexity",
    label="Maximum complexity",
    description="The maximum number of features that can be combined.",
    domain=IntegerSet.closedopen(1, 7),
    enabled=False,
    default_value=4,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
model_size_reg = MixedNode(
    name="model_size_reg",
    label="Model size regularization coefficient",
    description="This parameter influences the model size if training data has categorical features.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 10.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
nan_mode = CategoricalNode(
    name="nan_mode",
    label="NaN mode",
    description="The method for  processing missing values in the input dataset.",
    domain=CategoricalSet(categories={"Max", "Forbidden", "Min"}),
    enabled=False,
    default_value="Min",
    constraint=False,
    constraintInformation=None,
)
od_type = CategoricalNode(
    name="od_type",
    label="Overfitting detector type",
    description="The type of the overfitting detector to use.",
    domain=CategoricalSet(categories={"IncToDec", "Iter"}),
    enabled=False,
    default_value="IncToDec",
    constraint=False,
    constraintInformation=None,
)
od_wait = MixedNode(
    name="od_wait",
    label="Overfitting detector wait",
    description="The number of iterations to continue the training after the iteration with the optimal metric value.",
    domain=MixedSet(
        float_set=FloatSet(),
        integer_set=IntegerSet.closedopen(1, 31),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
random_strength = FloatNode(
    name="random_strength",
    label="Random strength",
    description="The amount of randomness to use for scoring splits when the tree structure is selected. Use this parameter to avoid overfitting the model.",
    domain=FloatSet.closed(0.0, 10.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
rsm = MixedNode(
    name="rsm",
    label="RSM",
    description="Random subspace method. The percentage of features to use at each split selection, when features are selected over again at random.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.01, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    allow_const_label,
    auto_class_weights,
    bagging_temperature,
    depth,
    feature_border_type,
    final_ctr_computation_mode,
    fold_len_multiplier,
    fold_permutation_block,
    has_time,
    iterations,
    l2_leaf_reg,
    learning_rate,
    max_ctr_complexity,
    model_size_reg,
    nan_mode,
    od_type,
    od_wait,
    random_strength,
    rsm,
]
