from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


alpha = FloatNode(
    name="alpha",
    label="Alpha",
    description="Constant that multiplies the penalty terms.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
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
l1_ratio = FloatNode(
    name="l1_ratio",
    label="L1 ratio",
    description="The Elastic-Net mixing parameter, with 0 <= l1_ratio <= 1.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(1, 5001),
    enabled=True,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
positive = CategoricalNode(
    name="positive",
    label="Positive",
    description="When set to True, forces the coefficients to be positive.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
selection = CategoricalNode(
    name="selection",
    label="Selection",
    description="If set to 'random', a random coefficient is updated every iteration rather than looping over features sequentially by default. This (setting to 'random') often leads to significantly faster convergence especially when tol is higher than 1e-4.",
    domain=CategoricalSet(categories={"cyclic", "random"}),
    enabled=False,
    default_value="cyclic",
    constraint=False,
    constraintInformation=None,
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0, 0.1),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    alpha,
    fit_intercept,
    l1_ratio,
    max_iter,
    positive,
    selection,
    tol,
]
