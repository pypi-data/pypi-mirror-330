from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


boosting_type = CategoricalNode(
    name="boosting_type",
    label="Boosting type",
    description="The type of boosting to use.",
    domain=CategoricalSet(categories={"dart", "goss", "rf", "gbdt"}),
    enabled=False,
    default_value="gbdt",
    constraint=True,
    constraintInformation="When boosting_type is rf, subsample must be in (0, 1), and subsample_freq must be greater than or equal to 1. When boosting_type is goss, subsampling is not used. The subsample ratio is ignored and subsample_freq must be smaller than or equal to 0.",
)
class_weight = CategoricalNode(
    name="class_weight",
    label="Class weight",
    description="Weights associated with classes in the form {class_label: weight}. If not given, all classes are supposed to have weight one. The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y)).",
    domain=CategoricalSet(categories={"balanced", "None"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
colsample_bytree = FloatNode(
    name="colsample_bytree",
    label="Column subsample ratio by tree",
    description="The subsample ratio of columns when constructing each tree. Subsampling occurs once for every tree constructed.",
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
    description="Step size shrinkage used in update to prevents overfitting. After each boosting step, we can directly get the weights of new features, and eta shrinks the feature weights to make the boosting process more conservative.",
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
    description="The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.",
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
    description="Minimal number of data in one leaf. Can be used to deal with over-fitting.",
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
    description="Minimum sum of instance weight (hessian) needed in a child.",
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
    description="The minimal gain to perform split.",
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
    description="The number of base estimators in the ensemble.",
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
    description="The maximum number of leaves in one tree.",
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
    description="L1 regularization term on weights. Increasing this value will make model more conservative.",
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
    description="L2 regularization term on weights. Increasing this value will make model more conservative.",
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
    description="Subsample ratio of the training instances. Setting it to 0.5 means that LightGBM would randomly sample half of the training data prior to growing trees. and this will prevent overfitting. Subsampling will occur once in every boosting iteration.",
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
    description="Number of data that sampled to construct feature discrete bins.",
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
    description="Frequency for bagging.",
    domain=IntegerSet.closedopen(0, 11),
    enabled=False,
    default_value=0,
    constraint=True,
    constraintInformation="When boosting_type is rf, subsample_freq must be greater than or equal to 1. When boosting_type is goss, subsample_freq must be smaller than or equal to 0.",
    distribution="uniform",
)

parameter_nodes = [
    boosting_type,
    class_weight,
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
