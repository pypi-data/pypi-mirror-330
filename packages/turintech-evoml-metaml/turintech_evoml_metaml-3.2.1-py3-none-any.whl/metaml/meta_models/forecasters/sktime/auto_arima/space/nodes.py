from metaml.parameter_space.node import CategoricalNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, IntegerSet


information_criterion = CategoricalNode(
    name="information_criterion",
    label="Information Criterion",
    description="The information criterion used to find the best SARIMAX model.",
    domain=CategoricalSet(categories={"aic", "hqic", "bic", "oob"}),
    enabled=False,
    default_value="aic",
    constraint=False,
    constraintInformation=None,
)
sp = IntegerNode(
    name="sp",
    label="Seasonal Period",
    description="The number of time steps in a complete seasonal cycle.",
    domain=IntegerSet.closedopen(1, 13),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    information_criterion,
    sp,
]
