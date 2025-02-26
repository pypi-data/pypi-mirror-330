from metaml.parameter_space.node import IntegerNode, CategoricalNode
from metaml.parameter_space.set import IntegerSet, CategoricalSet


p = IntegerNode(
    name="p",
    label="p",
    description="The order of the GARCH terms (past conditional variances or lagged forecast errors in variance) in the GARCH(p, q) model.",
    domain=IntegerSet.closedopen(1, 4),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
q = IntegerNode(
    name="q",
    label="q",
    description="The order of the ARCH terms (past squared error terms or lagged squared residuals from the mean equation) in the GARCH(p, q) model.",
    domain=IntegerSet.closedopen(0, 4),
    enabled=False,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    p,
    q,
]
