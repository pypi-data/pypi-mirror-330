from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


C = FloatNode(
    name="C",
    label="C",
    description="Weight of the loss term.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
alpha = FloatNode(
    name="alpha",
    label="Alpha",
    description="Weight of the penalty term.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
eta = FloatNode(
    name="eta",
    label="Eta",
    description="Decrease factor for line-search procedure.",
    domain=FloatSet.closed(0.0, 5.0),
    enabled=False,
    default_value=2.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="Maximum number of iterations to perform.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_steps = IntegerNode(
    name="max_steps",
    label="Maximum number of steps",
    description="Maximum number of steps to use during the line search.",
    domain=IntegerSet.closedopen(1, 101),
    enabled=False,
    default_value=30,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
penalty = CategoricalNode(
    name="penalty",
    label="Loss",
    description="The loss function to be used.",
    domain=CategoricalSet(categories={"l1", "simplex", "tv1d", "l1/l2"}),
    enabled=True,
    default_value="l1",
    constraint=False,
    constraintInformation=None,
)
sigma = FloatNode(
    name="sigma",
    label="Eta",
    description="Constant used in the line search sufficient decrease condition.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1e-05,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    C,
    alpha,
    eta,
    max_iter,
    max_steps,
    penalty,
    sigma,
]
