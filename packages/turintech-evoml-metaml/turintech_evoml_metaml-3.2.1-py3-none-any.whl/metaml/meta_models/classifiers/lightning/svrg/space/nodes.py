from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


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
    description="Step size for the gradient updates.",
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
    description="Kernel coefficient for rbf and poly kernels. Ignored by other kernels.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="The loss function to be used.",
    domain=CategoricalSet(categories={"modified_huber", "squared", "log", "squared_hinge", "smooth_hinge"}),
    enabled=True,
    default_value="smooth_hinge",
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="Maximum number of iterations to perform.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_inner = FloatNode(
    name="n_inner",
    label="Number of inner samples",
    description="Number of inner samples.",
    domain=FloatSet.closed(0.001, 1.0),
    enabled=False,
    default_value=1.0,
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
    eta,
    gamma,
    loss,
    max_iter,
    n_inner,
    tol,
]
