from metaml.parameter_space.node import CategoricalNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, IntegerSet


season_length = IntegerNode(
    name="season_length",
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
    season_length,
]
