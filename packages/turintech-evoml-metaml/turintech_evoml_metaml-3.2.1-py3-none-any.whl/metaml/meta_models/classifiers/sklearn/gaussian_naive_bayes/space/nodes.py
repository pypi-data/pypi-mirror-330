from metaml.parameter_space.node import FloatNode
from metaml.parameter_space.set import FloatSet


var_smoothing = FloatNode(
    name="var_smoothing",
    label="Var smoothing",
    description="Portion of the largest variance of all features that is added to variances for calculation stability.",
    domain=FloatSet.closed(1e-09, 1.0),
    enabled=True,
    default_value=1e-09,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    var_smoothing,
]
