from metaml.parameter_space.node import (
    CategoricalNode,
    FloatNode,
    IntegerNode,
    MixedNode,
)
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


bootstrap = CategoricalNode(
    name="bootstrap",
    label="Bootstrap",
    description="Indicates if bootstrap samples are used when building trees. If set to False, the entire dataset is used to build each tree, which may lead to overfitting.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=True,
    constraintInformation="When oob_score is True, bootstrap must be True. When bootstrap is False, max_samples must be None.",
)
ccp_alpha = FloatNode(
    name="ccp_alpha",
    label="Cost-Complexity Pruning alpha",
    description="The complexity parameter for Minimal Cost-Complexity Pruning, which helps prevent overfitting by pruning the tree. Larger values of alpha result in more aggressive pruning. By default, no pruning is performed.",
    domain=FloatSet.closed(0.0, 0.05),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
criterion = CategoricalNode(
    name="criterion",
    label="Criterion",
    description="The function used to measure the quality of a split in a decision tree.",
    domain=CategoricalSet(categories={"poisson", "absolute_error", "squared_error"}),
    enabled=False,
    default_value="squared_error",
    constraint=False,
    constraintInformation=None,
)
max_depth = IntegerNode(
    name="max_depth",
    label="Maximum depth",
    description="The maximum depth allowed for each tree, which helps prevent overfitting by limiting complexity.",
    domain=IntegerSet.closedopen(3, 17),
    enabled=True,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_features = MixedNode(
    name="max_features",
    label="Maximum features",
    description="Specifies the maximum number of features to consider when making a split in each decision tree, introducing randomness and diversity among the trees to improve the model's generalization ability. ",
    domain=MixedSet(
        categorical_set=CategoricalSet({"sqrt", "log2"}),
        float_set=FloatSet.closed(0.1, 1.0),
    ),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
)
max_leaf_nodes = IntegerNode(
    name="max_leaf_nodes",
    label="Maximum number of nodes",
    description="The maximum number of leaf nodes allowed in each tree, grown in a best-first fashion. Limits the number of leaf nodes in each decision tree, controlling the tree's complexity and helping to prevent overfitting.",
    domain=IntegerSet.closedopen(2, 1025),
    enabled=False,
    default_value=1024,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_samples = MixedNode(
    name="max_samples",
    label="Maximum samples",
    description="The number of samples randomly drawn from the input data to train each base estimator.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.1, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value=1.0,
    constraint=True,
    constraintInformation="When bootstrap is False, max_samples must be None.",
)
min_impurity_decrease = FloatNode(
    name="min_impurity_decrease",
    label="Minimum impurity decrease",
    description="The minimum decrease in impurity required for a node to be split. Helps prevent overfitting by controlling tree growth.",
    domain=FloatSet.closed(0.0, 0.1),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_samples_leaf = FloatNode(
    name="min_samples_leaf",
    label="Minimum samples per leaf",
    description="The minimum number of samples required for a node to be considered a leaf. This parameter helps prevent overfitting by ensuring that leaves have a sufficient number of samples.",
    domain=FloatSet.closed(0.0001, 0.05),
    enabled=False,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_samples_split = IntegerNode(
    name="min_samples_split",
    label="Minimum sample split",
    description="The minimum number of samples required to split an internal node, which helps control the growth of the tree and prevent overfitting.",
    domain=IntegerSet.closed(2, 20),
    enabled=False,
    default_value=2,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_weight_fraction_leaf = FloatNode(
    name="min_weight_fraction_leaf",
    label="Minimum weighted sum per leaf",
    description="The minimum weighted fraction of the total sample weights required for a node to be considered a leaf. By default, all samples have equal weight.",
    domain=FloatSet.closed(0.0, 0.01),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_estimators = IntegerNode(
    name="n_estimators",
    label="Number of estimators",
    description="The number of decision trees in the ensemble, which affects the model's performance and complexity.",
    domain=IntegerSet.closedopen(10, 201),
    enabled=True,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    bootstrap,
    ccp_alpha,
    criterion,
    max_depth,
    max_features,
    max_leaf_nodes,
    max_samples,
    min_impurity_decrease,
    min_samples_leaf,
    min_samples_split,
    min_weight_fraction_leaf,
    n_estimators,
]
