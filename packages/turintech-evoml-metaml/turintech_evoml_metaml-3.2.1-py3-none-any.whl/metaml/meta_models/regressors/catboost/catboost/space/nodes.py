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
    description="Allows training with datasets that have equal label values for all objects.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
approx_on_full_history = CategoricalNode(
    name="approx_on_full_history",
    label="Approximation on full history",
    description="Determines whether approximated values are calculated using all preceding rows in the fold or only a fraction of them.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=True,
    constraintInformation="When boosting_type is Plain, approx_on_full_history must be False.",
)
bagging_temperature = MixedNode(
    name="bagging_temperature",
    label="Bagging temperature",
    description="Controls the intensity of Bayesian bagging, with higher values resulting in more aggressive bagging.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=True,
    constraintInformation="When bootstrap_type is Bayesian or Bernoulli, bagging_temperature must be None.",
)
boost_from_average = CategoricalNode(
    name="boost_from_average",
    label="Boost from average",
    description="Initializes approximated values with the best constant value for the specified loss function.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=True,
    constraintInformation="When boost_from_average is True, model_shrink_rate must be None.",
)
boosting_type = CategoricalNode(
    name="boosting_type",
    label="Boosting type",
    description="Specifies the boosting scheme, either 'Ordered' for better quality or 'Plain' for classic gradient boosting.",
    domain=CategoricalSet(categories={"None", "Plain", "Ordered"}),
    enabled=False,
    default_value="None",
    constraint=True,
    constraintInformation="When boosting_type is Plain, approx_on_full_history must be False.",
)
bootstrap_type = CategoricalNode(
    name="bootstrap_type",
    label="Bootstrap type",
    description="Determines the method used for sampling the data during the training process to create a diverse ensemble of weak learners.",
    domain=CategoricalSet(categories={"Bernoulli", "MVS", "Bayesian"}),
    enabled=False,
    default_value="MVS",
    constraint=True,
    constraintInformation="When bootstrap_type is Bayesian or Bernoulli, bagging_temperature must be None. When bootstrap_type is Bayesian, subsample must be None.",
)
counter_calc_method = CategoricalNode(
    name="counter_calc_method",
    label="Counter calc method",
    description="Specifies the method used for calculating counters (statistics-based encodings) for categorical features, which generates new features enabling better capture of the relationship between categorical features and the target variable.",
    domain=CategoricalSet(categories={"Full", "SkipTest", "None"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
depth = IntegerNode(
    name="depth",
    label="Depth",
    description="Sets the maximum depth of the decision trees in the ensemble.",
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
    description="Determines the quantization mode for numerical features.",
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
fold_len_multiplier = MixedNode(
    name="fold_len_multiplier",
    label="Fold length multiplier",
    description="Adjusts the length of folds by a specified coefficient.",
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
    description="Sets the size of blocks for grouping objects in the dataset before random permutations.",
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
    description="Uses the order of objects in the input data without performing random permutations during certain stages.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
iterations = IntegerNode(
    name="iterations",
    label="Iterations",
    description="Sets the number of iterations for the model.",
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
    description="Specifies the coefficient for the L2 regularization term of the cost function.",
    domain=FloatSet.closed(0.0, 10.0),
    enabled=True,
    default_value=3.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
leaf_estimation_backtracking = CategoricalNode(
    name="leaf_estimation_backtracking",
    label="Leaf estimation backtracking",
    description="Determines the backtracking behavior when leaf_estimation_iterations is greater than 1.",
    domain=CategoricalSet(categories={"No", "AnyImprovement"}),
    enabled=False,
    default_value="AnyImprovement",
    constraint=False,
    constraintInformation=None,
)
learning_rate = MixedNode(
    name="learning_rate",
    label="Learning rate",
    description="Sets the step size shrinkage to prevent overfitting during the boosting process.",
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
    description="The maximum number of categorical features that can be combined to generate numerical features during the training process.",
    domain=IntegerSet.closedopen(1, 7),
    enabled=False,
    default_value=4,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
model_shrink_rate = MixedNode(
    name="model_shrink_rate",
    label="Model shrink rate",
    description="Enables model shrinkage at the start of each iteration, which reduces the influence of the most recently added weak learners and helps prevent overfitting.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 0.999),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=True,
    constraintInformation="When boost_from_average is True, model_shrink_rate must be None.",
)
model_size_reg = MixedNode(
    name="model_size_reg",
    label="Model size regularization coefficient",
    description="Influences the model size when training data contains categorical features.",
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
    description="Specifies the method for processing missing values in the input dataset.",
    domain=CategoricalSet(categories={"Max", "Forbidden", "Min"}),
    enabled=False,
    default_value="Min",
    constraint=False,
    constraintInformation=None,
)
od_type = CategoricalNode(
    name="od_type",
    label="Overfitting detector type",
    description="Sets the type of overfitting detector to use.",
    domain=CategoricalSet(categories={"IncToDec", "Iter"}),
    enabled=False,
    default_value="IncToDec",
    constraint=False,
    constraintInformation=None,
)
od_wait = MixedNode(
    name="od_wait",
    label="Overfitting detector wait",
    description="Determines the number of iterations to continue training after the iteration with the optimal metric value.",
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
    description="Sets the amount of randomness used for scoring splits during tree structure selection to avoid overfitting.",
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
    description="Specifies the percentage of features to use at each split selection with random subspace method.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.01, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=True,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
score_function = CategoricalNode(
    name="score_function",
    label="Score function",
    description="Defines the score type used to select the next split during tree construction.",
    domain=CategoricalSet(categories={"Cosine", "L2"}),
    enabled=False,
    default_value="Cosine",
    constraint=False,
    constraintInformation=None,
)
subsample = MixedNode(
    name="subsample",
    label="Subsample",
    description="Determines the fraction of the training dataset randomly sampled without replacement for training each weak learner, introducing diversity and reducing overfitting.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.4, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=True,
    constraintInformation="When bootstrap_type is Bayesian, subsample must be None.",
)

parameter_nodes = [
    allow_const_label,
    approx_on_full_history,
    bagging_temperature,
    boost_from_average,
    boosting_type,
    bootstrap_type,
    counter_calc_method,
    depth,
    feature_border_type,
    fold_len_multiplier,
    fold_permutation_block,
    has_time,
    iterations,
    l2_leaf_reg,
    leaf_estimation_backtracking,
    learning_rate,
    max_ctr_complexity,
    model_shrink_rate,
    model_size_reg,
    nan_mode,
    od_type,
    od_wait,
    random_strength,
    rsm,
    score_function,
    subsample,
]
