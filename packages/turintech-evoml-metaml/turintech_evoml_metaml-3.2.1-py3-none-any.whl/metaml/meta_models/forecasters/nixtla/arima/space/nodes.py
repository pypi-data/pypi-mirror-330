from metaml.parameter_space.node import IntegerNode, CategoricalNode, MixedNode
from metaml.parameter_space.set import IntegerSet, CategoricalSet, MixedSet, FloatSet


D = IntegerNode(
    name="D",
    label="D",
    description="The degree of seasonal differencing.",
    domain=IntegerSet.closedopen(0, 2),
    enabled=False,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
P = IntegerNode(
    name="P",
    label="P",
    description="The order of the seasonal autoregressive term.",
    domain=IntegerSet.closedopen(0, 3),
    enabled=False,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
Q = IntegerNode(
    name="Q",
    label="Q",
    description="The order of the seasonal moving average term.",
    domain=IntegerSet.closedopen(0, 3),
    enabled=False,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
d = IntegerNode(
    name="d",
    label="d",
    description="The degree of differencing.",
    domain=IntegerSet.closedopen(0, 3),
    enabled=False,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
p = IntegerNode(
    name="p",
    label="p",
    description="The order of the autoregressive term.",
    domain=IntegerSet.closedopen(0, 6),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
q = IntegerNode(
    name="q",
    label="q",
    description="The order of the moving average term.",
    domain=IntegerSet.closedopen(0, 6),
    enabled=False,
    default_value=0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
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
include_mean = CategoricalNode(
    name="include_mean",
    label="Include Mean",
    description="Whether or not to include a mean term.",
    domain=CategoricalSet([True, False]),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
include_drift = CategoricalNode(
    name="include_drift",
    label="Include Drift",
    description="Whether or not to include a drift term.",
    domain=CategoricalSet([True, False]),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
blambda = MixedNode(
    name="blambda",
    label="Box-Cox Lambda",
    description="The Box-Cox transformation parameter.",
    domain=MixedSet(
        float_set=FloatSet.closedopen(0, 2),
        categorical_set=CategoricalSet(["None"]),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
biasadj = CategoricalNode(
    name="biasadj",
    label="Bias Adjustment",
    description="Use adjusted back-transformed mean Box-Cox.",
    domain=CategoricalSet([True, False]),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)


parameter_nodes = [
    D,
    P,
    Q,
    d,
    p,
    q,
    season_length,
    include_mean,
    include_drift,
    blambda,
    biasadj,
]
