from metaml.parameter_space.node import (
    CategoricalNode,
    FloatNode,
    IntegerNode,
    MixedNode,
)
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


ccp_alpha = FloatNode(
    name="ccp_alpha",
    label="Cost-Complexity Pruning alpha",
    description="Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen. By default, no pruning is performed.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
criterion = CategoricalNode(
    name="criterion",
    label="Criterion",
    description="The function to measure the quality of a split.",
    domain=CategoricalSet(categories={"friedman_mse", "squared_error"}),
    enabled=False,
    default_value="friedman_mse",
    constraint=False,
    constraintInformation=None,
)
learning_rate = FloatNode(
    name="learning_rate",
    label="Learning rate",
    description="Step size shrinkage used in update to prevents overfitting. After each boosting step, we can directly get the weights of new features, and eta shrinks the feature weights to make the boosting process more conservative.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="Loss function to be optimized.",
    domain=CategoricalSet(categories={"exponential", "log_loss"}),
    enabled=False,
    default_value="log_loss",
    constraint=False,
    constraintInformation=None,
)
max_depth = IntegerNode(
    name="max_depth",
    label="Maximum depth",
    description="The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.",
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
    description="The number of features to draw from X to train each base estimator.",
    domain=MixedSet(
        categorical_set=CategoricalSet({"log2", "sqrt"}),
        float_set=FloatSet.closed(0.1, 1.0),
    ),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
)
max_leaf_nodes = IntegerNode(
    name="max_leaf_nodes",
    label="Maximum number of nodes",
    description="Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.",
    domain=IntegerSet.closedopen(2, 1025),
    enabled=True,
    default_value=1024,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_impurity_decrease = FloatNode(
    name="min_impurity_decrease",
    label="Minimum impurity decrease",
    description="A node will be split if this split induces a decrease of the impurity greater than or equal to this value.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_samples_leaf = FloatNode(
    name="min_samples_leaf",
    label="Minimum samples per leaf",
    description="The minimum number of samples required to be at a leaf node expressed as a fraction of all training samples.",
    domain=FloatSet.closed(0.0001, 0.5),
    enabled=False,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_samples_split = FloatNode(
    name="min_samples_split",
    label="Minimum sample split",
    description="The minimum number of samples required to split an internal node expressed as a fraction of all training samples.",
    domain=FloatSet.closed(0.0001, 0.5),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_weight_fraction_leaf = FloatNode(
    name="min_weight_fraction_leaf",
    label="Minimum weighted sum per leaf",
    description="The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node. Samples have equal weight when sample_weight is not provided.",
    domain=FloatSet.closed(0.0, 0.5),
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
    domain=IntegerSet.closedopen(10, 201),
    enabled=False,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_iter_no_change = MixedNode(
    name="n_iter_no_change",
    label="Maximum number of iterations with no change",
    description="Maximum number of epochs to not meet tol improvement. Only effective when solver='sgd' or 'adam'.",
    domain=MixedSet(
        float_set=FloatSet(),
        integer_set=IntegerSet.closedopen(10, 21),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
subsample = FloatNode(
    name="subsample",
    label="Subsample",
    description="Subsample ratio of the training instances. Setting it to 0.5 means that XGBoost would randomly sample half of the training data prior to growing trees. and this will prevent overfitting. Subsampling will occur once in every boosting iteration.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0001, 0.1),
    enabled=False,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
validation_fraction = FloatNode(
    name="validation_fraction",
    label="Validation fraction",
    description="The proportion of training data to set aside as validation set for early stopping.",
    domain=FloatSet.closed(0.0, 0.9999),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    ccp_alpha,
    criterion,
    learning_rate,
    loss,
    max_depth,
    max_features,
    max_leaf_nodes,
    min_impurity_decrease,
    min_samples_leaf,
    min_samples_split,
    min_weight_fraction_leaf,
    n_estimators,
    n_iter_no_change,
    subsample,
    tol,
    validation_fraction,
]
