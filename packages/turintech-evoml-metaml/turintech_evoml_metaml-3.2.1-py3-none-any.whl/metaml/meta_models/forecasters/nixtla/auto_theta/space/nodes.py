from metaml.parameter_space.node import IntegerNode, CategoricalNode
from metaml.parameter_space.set import IntegerSet, CategoricalSet


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
decomposition_type = CategoricalNode(
    name="decomposition_type",
    label="Decomposition Type",
    description="The type of seasonal decomposition to use.",
    domain=CategoricalSet(["additive", "multiplicative"]),
    enabled=False,
    default_value="multiplicative",
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    season_length,
    decomposition_type,
]
