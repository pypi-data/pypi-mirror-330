from metaml.parameter_space.node import CategoricalNode, FloatNode, MixedNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


shrinkage = MixedNode(
    name="shrinkage",
    label="Shrinkage",
    description="Shrinkage parameter.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=True,
    constraintInformation="When solver is svd, shrinkage must be None.",
)
solver = CategoricalNode(
    name="solver",
    label="Solver",
    description="Solver to use.",
    domain=CategoricalSet(categories={"svd", "lsqr", "eigen"}),
    enabled=False,
    default_value="svd",
    constraint=True,
    constraintInformation="When solver is svd, shrinkage must be None.",
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
    shrinkage,
    solver,
    tol,
]
