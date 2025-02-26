from metaml.parameter_space.node import IntegerNode
from metaml.parameter_space.set import IntegerSet


sp = IntegerNode(
    name="sp",
    label="Seasonal periodicity.",
    description="The number steps in the series which make up one seasonal cycle.",
    domain=IntegerSet.closedopen(1, 13),
    enabled=True,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    sp,
]
