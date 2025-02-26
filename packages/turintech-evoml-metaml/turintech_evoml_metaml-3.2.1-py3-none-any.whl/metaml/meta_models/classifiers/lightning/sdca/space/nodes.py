from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


alpha = FloatNode(
    name="alpha",
    label="Alpha",
    description="Amount of regularization.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
gamma = FloatNode(
    name="gamma",
    label="Gamma",
    description="Gamma parameter in the 'smooth_hinge' loss (not used for other loss functions).",
    domain=FloatSet.closed(0.001, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
l1_ratio = FloatNode(
    name="l1_ratio",
    label="L1 ratio",
    description="Ratio between the L1 and L2 regularization.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="The loss function to be used.",
    domain=CategoricalSet(categories={"squared", "squared_hinge", "hinge", "absolute", "smooth_hinge"}),
    enabled=True,
    default_value="hinge",
    constraint=False,
    constraintInformation=None,
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
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Tolerance of the stopping criterion.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    alpha,
    gamma,
    l1_ratio,
    loss,
    max_iter,
    tol,
]
