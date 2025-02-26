from metaml.parameter_space.node import IntegerNode
from metaml.parameter_space.set import IntegerSet


sp = IntegerNode(
    name="sp",
    label="Seasonal Period",
    description="The number of time steps in a complete cycle.",
    domain=IntegerSet.closedopen(1, 53),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    sp,
]
