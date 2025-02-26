from metaml.parameter_space.node import FloatNode
from metaml.parameter_space.set import FloatSet


reg_param = FloatNode(
    name="reg_param",
    label="Regularise covariance estimates",
    description="Regularizes the per-class covariance estimates by transforming S2 as S2 = (1 - reg_param) * S2 + reg_param * np.eye(n_features), where S2 corresponds to the scaling_ attribute of a given class.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    reg_param,
    tol,
]
