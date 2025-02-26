from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


alpha = FloatNode(
    name="alpha",
    label="Alpha",
    description="Constant that multiplies the penalty terms.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
epsilon = FloatNode(
    name="epsilon",
    label="Epsilon",
    description="Value for numerical stability in adam. Only used when solver='adam'.",
    domain=FloatSet.closed(1.01, 3.0),
    enabled=False,
    default_value=1.35,
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
    domain=IntegerSet.closedopen(1, 501),
    enabled=True,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(1e-05, 1.0),
    enabled=True,
    default_value=1e-05,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    alpha,
    epsilon,
    fit_intercept,
    max_iter,
    tol,
]
