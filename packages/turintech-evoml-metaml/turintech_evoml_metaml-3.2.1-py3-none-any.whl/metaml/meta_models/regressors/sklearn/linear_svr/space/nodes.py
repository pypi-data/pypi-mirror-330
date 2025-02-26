from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


C = FloatNode(
    name="C",
    label="C",
    description="Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.",
    domain=FloatSet.closed(0.0, 25.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
dual = CategoricalNode(
    name="dual",
    label="Dual",
    description="Select the algorithm to either solve the dual or primal optimization problem. Prefer dual=False when n_samples > n_features.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=True,
    constraintInformation="When dual is False, loss must be squared_epsilon_insensitive.",
)
epsilon = FloatNode(
    name="epsilon",
    label="Epsilon",
    description="Value for numerical stability in adam. Only used when solver='adam'.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.0,
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
intercept_scaling = FloatNode(
    name="intercept_scaling",
    label="Intercept scaling",
    description="Useful only when the solver 'liblinear' is used and self.fit_intercept is set to True. In this case, x becomes [x, self.intercept_scaling], i.e. a “synthetic” feature with constant value equal to intercept_scaling is appended to the instance vector. The intercept becomes intercept_scaling * synthetic_feature_weight.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="Specifies the loss function. The epsilon-insensitive loss (standard SVR) is the L1 loss, while the squared epsilon-insensitive loss (squared_epsilon_insensitive) is the L2 loss.",
    domain=CategoricalSet(categories={"epsilon_insensitive", "squared_epsilon_insensitive"}),
    enabled=False,
    default_value="epsilon_insensitive",
    constraint=True,
    constraintInformation="When dual is False, loss must be squared_epsilon_insensitive.",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(500, 2001),
    enabled=True,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    C,
    dual,
    epsilon,
    fit_intercept,
    intercept_scaling,
    loss,
    max_iter,
    tol,
]
