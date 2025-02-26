from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


l2_regularization = FloatNode(
    name="l2_regularization",
    label="L2 regularization",
    description="The L2 regularization parameter. Use 0 for no regularization.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
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
    domain=CategoricalSet(categories={"auto", "binary_crossentropy", "categorical_crossentropy"}),
    enabled=True,
    default_value="auto",
    constraint=False,
    constraintInformation=None,
)
max_bins = IntegerNode(
    name="max_bins",
    label="Maximum bins",
    description="The maximum number of bins to use for non-missing values.",
    domain=IntegerSet.closedopen(2, 256),
    enabled=False,
    default_value=255,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
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
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(0, 201),
    enabled=False,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_leaf_nodes = IntegerNode(
    name="max_leaf_nodes",
    label="Maximum number of nodes",
    description="Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.",
    domain=IntegerSet.closedopen(2, 101),
    enabled=True,
    default_value=31,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_samples_leaf = IntegerNode(
    name="min_samples_leaf",
    label="Minimum samples per leaf",
    description="The minimum number of samples required to be at a leaf node.",
    domain=IntegerSet.closedopen(0, 51),
    enabled=False,
    default_value=20,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_iter_no_change = IntegerNode(
    name="n_iter_no_change",
    label="Maximum number of iterations with no change",
    description="Maximum number of epochs to not meet tol improvement. Only effective when solver='sgd' or 'adam'.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(1e-07, 1.0),
    enabled=True,
    default_value=1e-07,
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
    l2_regularization,
    learning_rate,
    loss,
    max_bins,
    max_depth,
    max_iter,
    max_leaf_nodes,
    min_samples_leaf,
    n_iter_no_change,
    tol,
    validation_fraction,
]
