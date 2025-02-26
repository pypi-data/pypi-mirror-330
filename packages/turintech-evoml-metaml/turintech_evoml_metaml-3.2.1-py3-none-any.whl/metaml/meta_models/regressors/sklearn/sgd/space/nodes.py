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
average = CategoricalNode(
    name="average",
    label="Average",
    description="When set to True, computes the averaged SGD weights accross all updates and stores the result in the coef_ attribute.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
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
epsilon = FloatNode(
    name="epsilon",
    label="Epsilon",
    description="Value for numerical stability in adam. Only used when solver='adam'.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
eta0 = FloatNode(
    name="eta0",
    label="Eta0",
    description="The initial learning rate for the 'constant', 'invscaling' or 'adaptive' schedules.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.01,
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
l1_ratio = FloatNode(
    name="l1_ratio",
    label="L1 ratio",
    description="The Elastic-Net mixing parameter, with 0 <= l1_ratio <= 1.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.15,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
learning_rate = CategoricalNode(
    name="learning_rate",
    label="Learning rate",
    description="Step size shrinkage used in update to prevents overfitting. After each boosting step, we can directly get the weights of new features, and eta shrinks the feature weights to make the boosting process more conservative.",
    domain=CategoricalSet(categories={"constant", "adaptive", "optimal", "invscaling"}),
    enabled=False,
    default_value="invscaling",
    constraint=False,
    constraintInformation=None,
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="Loss function to be optimized.",
    domain=CategoricalSet(
        categories={
            "squared_error",
            "epsilon_insensitive",
            "huber",
            "squared_epsilon_insensitive",
        }
    ),
    enabled=True,
    default_value="squared_error",
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(1, 2001),
    enabled=False,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_iter_no_change = IntegerNode(
    name="n_iter_no_change",
    label="Maximum number of iterations with no change",
    description="Maximum number of epochs to not meet tol improvement. Only effective when solver='sgd' or 'adam'.",
    domain=IntegerSet.closedopen(1, 101),
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
    domain=CategoricalSet(categories={"l1", "elasticnet", "l2"}),
    enabled=True,
    default_value="l2",
    constraint=False,
    constraintInformation=None,
)
power_t = FloatNode(
    name="power_t",
    label="Power t",
    description="The exponent for inverse scaling learning rate.",
    domain=FloatSet.closed(0.0, 50.0),
    enabled=False,
    default_value=0.25,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
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
    average,
    early_stopping,
    epsilon,
    eta0,
    fit_intercept,
    l1_ratio,
    learning_rate,
    loss,
    max_iter,
    n_iter_no_change,
    penalty,
    power_t,
    shuffle,
    tol,
    validation_fraction,
]
