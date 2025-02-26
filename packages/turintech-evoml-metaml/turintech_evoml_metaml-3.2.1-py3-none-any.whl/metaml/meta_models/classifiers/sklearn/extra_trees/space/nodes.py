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
    description="Whether bootstrap samples are used when building trees. If False, the whole dataset is used to build each tree.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=True,
    constraintInformation="When oob_score is True, bootstrap must be True.",
)
ccp_alpha = FloatNode(
    name="ccp_alpha",
    label="Cost-Complexity Pruning alpha",
    description="Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen. By default, no pruning is performed.",
    domain=FloatSet.closed(0.0, 0.1),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
class_weight = CategoricalNode(
    name="class_weight",
    label="Class weight",
    description="Sets the weights for all classes. If None, all classes are supposed to have weight one. The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y)). The “balanced_subsample” mode is the same as “balanced” except that weights are computed based on the bootstrap sample for every tree grown.",
    domain=CategoricalSet(categories={"balanced", "None", "balanced_subsample"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
criterion = CategoricalNode(
    name="criterion",
    label="Criterion",
    description="The function to measure the quality of a split.",
    domain=CategoricalSet(categories={"gini", "entropy"}),
    enabled=False,
    default_value="gini",
    constraint=False,
    constraintInformation=None,
)
max_depth = IntegerNode(
    name="max_depth",
    label="Maximum depth",
    description="The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.",
    domain=IntegerSet.closedopen(1, 17),
    enabled=True,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_features = CategoricalNode(
    name="max_features",
    label="Maximum features",
    description="The number of features to draw from X to train each base estimator.",
    domain=CategoricalSet({"log2", "sqrt"}),
    enabled=False,
    default_value="sqrt",
    constraint=False,
    constraintInformation=None,
)
max_leaf_nodes = IntegerNode(
    name="max_leaf_nodes",
    label="Maximum number of nodes",
    description="Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity.",
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
    description="The number of samples to draw from X to train each base estimator.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0001, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value=0.9999,
    constraint=True,
    constraintInformation="When bootstrap is False, max_samples must be None.",
)
min_impurity_decrease = FloatNode(
    name="min_impurity_decrease",
    label="Minimum impurity decrease",
    description="A node will be split if this split induces a decrease of the impurity greater than or equal to this value.",
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
    description="The minimum number of samples required to be at a leaf node.",
    domain=FloatSet.closed(0.0001, 0.1),
    enabled=False,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_samples_split = FloatNode(
    name="min_samples_split",
    label="Minimum sample split",
    description="The minimum number of samples required to split an internal node.",
    domain=FloatSet.closed(0.0001, 0.1),
    enabled=False,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_weight_fraction_leaf = FloatNode(
    name="min_weight_fraction_leaf",
    label="Minimum weighted sum per leaf",
    description="The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node. Samples have equal weight when sample_weight is not provided.",
    domain=FloatSet.closed(0.0, 0.1),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_estimators = IntegerNode(
    name="n_estimators",
    label="Number of estimators",
    description="The number of base estimators in the ensemble.",
    domain=IntegerSet.closedopen(10, 101),
    enabled=False,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    bootstrap,
    ccp_alpha,
    class_weight,
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
