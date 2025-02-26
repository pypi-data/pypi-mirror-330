from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


alpha = FloatNode(
    name="alpha",
    label="Alpha",
    description="Constant that multiplies the penalty terms.",
    domain=FloatSet.closed(0.0, 0.1),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
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
early_stopping = CategoricalNode(
    name="early_stopping",
    label="Early stopping",
    description="Whether to use early stopping to terminate training when validation score is not improving.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
eta0 = FloatNode(
    name="eta0",
    label="Eta0",
    description="The initial learning rate for the 'constant', 'invscaling' or 'adaptive' schedules.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Calculate Intercept",
    description="Whether to calculate the intercept for this model. If set to False, no intercept will be used in calculations (i.e. data is expected to be centered).",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(0, 2001),
    enabled=True,
    default_value=1000,
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
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
penalty = CategoricalNode(
    name="penalty",
    label="Penalty",
    description="The penalty (aka regularization term) to be used.",
    domain=CategoricalSet(categories={"None", "l1", "elasticnet", "l2"}),
    enabled=True,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
shuffle = CategoricalNode(
    name="shuffle",
    label="Shuffle",
    description="Whether to shuffle samples in each iteration.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.001,
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
    alpha,
    class_weight,
    early_stopping,
    eta0,
    fit_intercept,
    max_iter,
    n_iter_no_change,
    penalty,
    shuffle,
    tol,
    validation_fraction,
]
