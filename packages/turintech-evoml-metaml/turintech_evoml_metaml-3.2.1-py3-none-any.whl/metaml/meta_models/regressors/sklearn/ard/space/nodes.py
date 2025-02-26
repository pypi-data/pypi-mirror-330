from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


alpha_1 = FloatNode(
    name="alpha_1",
    label="Alpha 1",
    description="Shape parameter for the Gamma distribution prior over the alpha parameter, which influences the strength of the regularization.",
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
    description="Inverse scale parameter (rate parameter) for the Gamma distribution prior over the alpha parameter, which affects the distribution's shape and scale.",
    domain=FloatSet.closed(1e-06, 0.3),
    enabled=True,
    default_value=1e-06,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Calculate Intercept",
    description="Indicates whether to calculate the intercept for this model. If set to False, the data is expected to be centered and no intercept will be used in calculations.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
lambda_1 = FloatNode(
    name="lambda_1",
    label="Lambda 1",
    description="Shape parameter for the Gamma distribution prior over the lambda parameter, which influences the strength of the regularization for each feature's weight.",
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
    description="Inverse scale parameter (rate parameter) for the Gamma distribution prior over the lambda parameter, which affects the distribution's shape and scale for each feature's weight.",
    domain=FloatSet.closed(1e-06, 0.3),
    enabled=True,
    default_value=1e-06,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Number of iterations",
    description="Maximum number of iterations for the model to converge.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=300,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
threshold_lambda = FloatNode(
    name="threshold_lambda",
    label="Threshold lambda",
    description="Threshold for pruning weights with high precision from the computation, which can help in reducing model complexity.",
    domain=FloatSet.closed(0.0, 10000.0),
    enabled=True,
    default_value=10000.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Controls the stopping criterion in iterative algorithms, specifying the minimum improvement in the objective function or loss between consecutive iterations required for the algorithm to continue training.",
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
    fit_intercept,
    lambda_1,
    lambda_2,
    max_iter,
    threshold_lambda,
    tol,
]
