from metaml.parameter_space.node import CategoricalNode, MixedNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


metric = CategoricalNode(
    name="metric",
    label="Metric",
    description="The metric to use.",
    domain=CategoricalSet(categories={"euclidean"}),
    enabled=True,
    default_value="euclidean",
    constraint=False,
    constraintInformation=None,
)
shrink_threshold = MixedNode(
    name="shrink_threshold",
    label="Shrink threshold",
    description="Threshold for shrinking centroids to remove features.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=True,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    metric,
    shrink_threshold,
]
