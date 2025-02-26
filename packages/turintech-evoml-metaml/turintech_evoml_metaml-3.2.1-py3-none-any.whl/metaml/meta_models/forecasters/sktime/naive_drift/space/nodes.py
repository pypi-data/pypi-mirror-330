from metaml.parameter_space.node import IntegerNode
from metaml.parameter_space.set import IntegerSet


window_length = IntegerNode(
    name="window_length",
    label="Window length",
    description="The size of the window over which to calculate a rolling mean.",
    domain=IntegerSet.closedopen(1, 21),
    enabled=True,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    window_length,
]
