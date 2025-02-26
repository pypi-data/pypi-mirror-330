from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


boosting_type = CategoricalNode(
    name="boosting_type",
    label="Boosting type",
    description="Specifies the type of boosting algorithm to use, which determines how the model combines weak learners to form a strong learner.",
    domain=CategoricalSet(categories={"dart", "goss", "rf", "gbdt"}),
    enabled=False,
    default_value="gbdt",
    constraint=True,
    constraintInformation="When boosting_type is rf, subsample must be in (0, 1), and subsample_freq must be greater than or equal to 1. When boosting_type is goss, subsample_freq must be smaller than or equal to 0.",
)
colsample_bytree = FloatNode(
    name="colsample_bytree",
    label="Column subsample ratio by tree",
    description="The fraction of features to select for each tree, which helps in reducing overfitting and improving training speed.",
    domain=FloatSet.closed(0.1, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
learning_rate = FloatNode(
    name="learning_rate",
    label="Learning rate",
    description="The shrinkage factor applied to the weights of new features after each boosting step, which helps prevent overfitting.",
    domain=FloatSet.closed(0.01, 1.0),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_depth = IntegerNode(
    name="max_depth",
    label="Maximum depth",
    description="The maximum depth of each decision tree, which controls the complexity of the model and prevents overfitting.",
    domain=IntegerSet.closedopen(3, 17),
    enabled=True,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_child_samples = IntegerNode(
    name="min_child_samples",
    label="Minimum childs per sample",
    description="The minimum number of samples required in a leaf node, which helps prevent overfitting by controlling tree growth.",
    domain=IntegerSet.closedopen(2, 51),
    enabled=False,
    default_value=20,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_child_weight = FloatNode(
    name="min_child_weight",
    label="Minimum child weight",
    description="The minimum sum of instance weights (hessian) required in a child node, which affects the tree structure and prevents overfitting.",
    domain=FloatSet.closed(0.001, 0.25),
    enabled=False,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_split_gain = FloatNode(
    name="min_split_gain",
    label="Minimal gain to split",
    description="The minimum gain required to perform a split, which helps control the complexity of the model.",
    domain=FloatSet.closed(0.0, 5.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_estimators = IntegerNode(
    name="n_estimators",
    label="Number of estimators",
    description="The number of decision trees in the ensemble, which determines the overall complexity and capacity of the model.",
    domain=IntegerSet.closedopen(10, 201),
    enabled=True,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
num_leaves = IntegerNode(
    name="num_leaves",
    label="Number of leaves",
    description="The maximum number of leaves in a single decision tree, which controls the complexity of the tree and affects the model's accuracy.",
    domain=IntegerSet.closedopen(2, 101),
    enabled=True,
    default_value=31,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
reg_alpha = FloatNode(
    name="reg_alpha",
    label="Regularization alpha",
    description="The L1 regularization term applied to the weights, which helps prevent overfitting by encouraging sparsity in the model.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
reg_lambda = FloatNode(
    name="reg_lambda",
    label="Regularization lambda",
    description="The L2 regularization term applied to the weights, which helps prevent overfitting by penalizing large weights.",
    domain=FloatSet.closed(0.0, 10000.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
subsample = FloatNode(
    name="subsample",
    label="Subsample",
    description="The fraction of training instances to use for each boosting iteration, which helps prevent overfitting and improves training speed.",
    domain=FloatSet.closedopen(0.5, 1.0),
    enabled=False,
    default_value=0.9999,
    constraint=False,
    constraintInformation="When boosting_type is rf, subsample must be in (0, 1).",
    distribution="uniform",
)
subsample_for_bin = IntegerNode(
    name="subsample_for_bin",
    label="Subsamples to construct bin",
    description="The number of samples used to construct discrete bins for continuous features, which affects the speed and memory usage of the model.",
    domain=IntegerSet.closedopen(100, 1000001),
    enabled=False,
    default_value=200000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
subsample_freq = IntegerNode(
    name="subsample_freq",
    label="Subsample frequency",
    description="The frequency at which subsampling occurs during the boosting process, which helps control overfitting and training speed.",
    domain=IntegerSet.closedopen(0, 11),
    enabled=False,
    default_value=0,
    constraint=True,
    constraintInformation="When boosting_type is rf, subsample_freq must be greater than or equal to 1. When boosting_type is goss, subsample_freq must be smaller than or equal to 0.",
    distribution="uniform",
)

parameter_nodes = [
    boosting_type,
    colsample_bytree,
    learning_rate,
    max_depth,
    min_child_samples,
    min_child_weight,
    min_split_gain,
    n_estimators,
    num_leaves,
    reg_alpha,
    reg_lambda,
    subsample,
    subsample_for_bin,
    subsample_freq,
]
