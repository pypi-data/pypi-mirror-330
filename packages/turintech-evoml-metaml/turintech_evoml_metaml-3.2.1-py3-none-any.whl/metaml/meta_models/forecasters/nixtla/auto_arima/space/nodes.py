from metaml.parameter_space.node import CategoricalNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, IntegerSet


ic = CategoricalNode(
    name="ic",
    label="Information Criterion",
    description="The information criterion used to find the best SARIMAX model.",
    domain=CategoricalSet(categories={"aic", "aicc", "bic"}),
    enabled=False,
    default_value="aicc",
    constraint=False,
    constraintInformation=None,
)
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
    ic,
    season_length,
]
