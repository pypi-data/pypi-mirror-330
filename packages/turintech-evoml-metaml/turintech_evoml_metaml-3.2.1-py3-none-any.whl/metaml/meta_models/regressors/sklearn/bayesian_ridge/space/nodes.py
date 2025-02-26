from metaml.parameter_space.node import (
    CategoricalNode,
    FloatNode,
    IntegerNode,
    MixedNode,
)
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


alpha_1 = FloatNode(
    name="alpha_1",
    label="Alpha 1",
    description="Hyper-parameter : shape parameter for the Gamma distribution prior over the alpha parameter.",
    domain=FloatSet.closed(1e-06, 0.3),
    enabled=True,
    default_value=1e-06,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
alpha_2 = FloatNode(
    name="alpha_2",
    label="Alpha 2",
    description="Hyper-parameter : inverse scale parameter (rate parameter) for the Gamma distribution prior over the alpha parameter.",
    domain=FloatSet.closed(1e-06, 0.3),
    enabled=True,
    default_value=1e-06,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
alpha_init = MixedNode(
    name="alpha_init",
    label="Alpha init",
    description="Initial value for alpha (precision of the noise). If not set, alpha_init is 1/Var(y).",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Calculate Intercept",
    description="Whether to calculate the intercept for this model. If set to False, no intercept will be used in calculations (i.e. data is expected to be centered).",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
lambda_1 = FloatNode(
    name="lambda_1",
    label="Lambda 1",
    description="Hyper-parameter : shape parameter for the Gamma distribution prior over the lambda parameter.",
    domain=FloatSet.closed(1e-06, 0.3),
    enabled=True,
    default_value=1e-06,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
lambda_2 = FloatNode(
    name="lambda_2",
    label="Lambda 2",
    description="Hyper-parameter : inverse scale parameter (rate parameter) for the Gamma distribution prior over the lambda parameter.",
    domain=FloatSet.closed(1e-06, 0.3),
    enabled=True,
    default_value=1e-06,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
lambda_init = MixedNode(
    name="lambda_init",
    label="Lambda init",
    description="Initial value for lambda (precision of the weights). If not set, lambda_init is 1.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Number of iterations",
    description="Maximum number of iterations.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=300,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.001, 0.1),
    enabled=False,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    alpha_1,
    alpha_2,
    alpha_init,
    fit_intercept,
    lambda_1,
    lambda_2,
    lambda_init,
    max_iter,
    tol,
]
