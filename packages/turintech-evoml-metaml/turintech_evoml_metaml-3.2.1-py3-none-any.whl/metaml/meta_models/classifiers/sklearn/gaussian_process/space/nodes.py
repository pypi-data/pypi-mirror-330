from metaml.parameter_space.node import CategoricalNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, IntegerSet


max_iter_predict = IntegerNode(
    name="max_iter_predict",
    label="Maximum number of iterations",
    description="The maximum number of iterations in Newton's method for approximating the posterior during predict. Smaller values will reduce computation time at the cost of worse results.",
    domain=IntegerSet.closedopen(0, 201),
    enabled=True,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_restarts_optimizer = IntegerNode(
    name="n_restarts_optimizer",
    label="Number of restarts",
    description="The number of restarts of the optimizer for finding the kernel's parameters which maximize the log-marginal likelihood. The first run of the optimizer is performed from the kernel's initial parameters, the remaining ones (if any) from thetas sampled log-uniform randomly from the space of allowed theta-values. If greater than 0, all bounds must be finite. Note that n_restarts_optimizer == 0 implies that one run is performed.",
    domain=IntegerSet.closedopen(0, 11),
    enabled=True,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    max_iter_predict,
    n_restarts_optimizer,
]
