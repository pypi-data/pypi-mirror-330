from metaml.parameter_space.node import IntegerNode
from metaml.parameter_space.set import IntegerSet


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
sp = IntegerNode(
    name="sp",
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
    D,
    P,
    Q,
    d,
    p,
    q,
    sp,
]
