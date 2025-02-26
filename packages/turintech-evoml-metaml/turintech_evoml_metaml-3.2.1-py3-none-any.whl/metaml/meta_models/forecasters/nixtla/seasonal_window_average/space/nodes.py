from metaml.parameter_space.node import IntegerNode
from metaml.parameter_space.set import IntegerSet


season_length = IntegerNode(
    name="season_length",
    label="Season Length",
    description="Number of steps in a seasonal cycle.",
    domain=IntegerSet.closedopen(1, 6),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
window_size = IntegerNode(
    name="window_size",
    label="Window Size",
    description="Number of previous steps used to calculate the average.",
    domain=IntegerSet.closedopen(1, 6),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    season_length,
    window_size,
]
