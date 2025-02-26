from metaml.parameter_space.node import (
    CategoricalNode,
    FloatNode,
    IntegerNode,
    MixedNode,
)
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


C = FloatNode(
    name="C",
    label="C",
    description="Weight of the loss term.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
Cd = FloatNode(
    name="Cd",
    label="C when doing debiasing",
    description="Value of `C` when doing debiasing.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
alpha = FloatNode(
    name="alpha",
    label="Alpha",
    description="Weight of the penalty term.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
beta = FloatNode(
    name="beta",
    label="Beta",
    description="Multiplicative constant used in the backtracking line search.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
debiasing = CategoricalNode(
    name="debiasing",
    label="Debiasing",
    description="Whether to refit the model using l2 penalty (only useful if penalty='l1' or penalty='l1/l2').",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="The loss function to be used.",
    domain=CategoricalSet(categories={"squared", "log", "modified_huber", "squared_hinge"}),
    enabled=False,
    default_value="squared_hinge",
    constraint=True,
    constraintInformation="When multiclass is True, loss must be squared_hinge or log.",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="Maximum number of iterations to perform.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=50,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_steps = MixedNode(
    name="max_steps",
    label="Maximum number of steps",
    description="Maximum number of steps to use during the line search.",
    domain=MixedSet(
        float_set=FloatSet(),
        integer_set=IntegerSet.closedopen(1, 101),
        categorical_set=CategoricalSet(categories={"auto"}),
    ),
    enabled=False,
    default_value="auto",
    constraint=False,
    constraintInformation=None,
)
multiclass = CategoricalNode(
    name="multiclass",
    label="Multiclass",
    description="Whether to use a direct multiclass formulation (True) or one-vs-rest (False).",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=True,
    constraintInformation="When multiclass is True, penalty must be l1/l2 and loss must be squared_hinge or log.",
)
penalty = CategoricalNode(
    name="penalty",
    label="Penalty",
    description="The penalty to be used.",
    domain=CategoricalSet(categories={"l1", "l1/l2", "l2"}),
    enabled=False,
    default_value="l2",
    constraint=True,
    constraintInformation="When multiclass is True, penalty must be l1/l2.",
)
permute = CategoricalNode(
    name="permute",
    label="Permute",
    description="Whether to permute coordinates or not before cycling (only when selection='cyclic').",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
selection = CategoricalNode(
    name="selection",
    label="Selection",
    description="Strategy to use for selecting coordinates.",
    domain=CategoricalSet(categories={"cyclic", "uniform"}),
    enabled=False,
    default_value="cyclic",
    constraint=False,
    constraintInformation=None,
)
shrinking = CategoricalNode(
    name="shrinking",
    label="Shrinking",
    description="Whether to activate shrinking or not.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
sigma = FloatNode(
    name="sigma",
    label="Sigma",
    description="Constant used in the line search sufficient decrease condition.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.01,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
termination = CategoricalNode(
    name="termination",
    label="Termination",
    description="Stopping criterion to use.",
    domain=CategoricalSet(categories={"violation_sum", "violation_max"}),
    enabled=True,
    default_value="violation_sum",
    constraint=False,
    constraintInformation=None,
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Tolerance of the stopping criterion.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
warm_debiasing = CategoricalNode(
    name="warm_debiasing",
    label="Warm debiasing",
    description="Whether to warm-start the model or not when doing debiasing.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    C,
    Cd,
    alpha,
    beta,
    debiasing,
    loss,
    max_iter,
    max_steps,
    multiclass,
    penalty,
    permute,
    selection,
    shrinking,
    sigma,
    termination,
    tol,
    warm_debiasing,
]
