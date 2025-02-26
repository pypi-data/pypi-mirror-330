from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


C = FloatNode(
    name="C",
    label="C",
    description="Inverse of the regularization strength. Controls the trade-off between achieving a low training error and a low testing error. A smaller value creates a wider margin, which may result in more training errors but better generalization to the test data.",
    domain=FloatSet.closed(0.001, 10.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
coef0 = FloatNode(
    name="coef0",
    label="Coefficient 0",
    description="Affects the shape of the decision boundary in 'poly' and 'sigmoid' kernels. It represents the independent term in the kernel function.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
degree = IntegerNode(
    name="degree",
    label="Degree",
    description="Specifies the degree of the polynomial kernel function ('poly'). Higher degrees result in more complex decision boundaries. This parameter is ignored by all other kernels.",
    domain=IntegerSet.closedopen(0, 6),
    enabled=False,
    default_value=3,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
epsilon = FloatNode(
    name="epsilon",
    label="Epsilon",
    description="Defines the margin of tolerance within which no penalty is given to errors. It determines the width of the epsilon-insensitive zone used to fit the training data.",
    domain=FloatSet.closed(0.0001, 2.0),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
kernel = CategoricalNode(
    name="kernel",
    label="Kernel",
    description="Determines the kernel function used in the algorithm. The kernel function transforms the input data into a higher-dimensional space where a linear function is fitted.",
    domain=CategoricalSet(categories={"rbf", "poly", "sigmoid"}),
    enabled=True,
    default_value="rbf",
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="Sets the maximum number of iterations for the solver to converge. Early stopping may result in a suboptimal solution.",
    domain=IntegerSet.closedopen(1, 1001),
    enabled=True,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
shrinking = CategoricalNode(
    name="shrinking",
    label="Shrinking",
    description="Indicates whether to use the shrinking heuristic, which is a technique used to remove some of the constraints in the optimization problem to speed up training.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Specifies the tolerance for stopping criterion. The solver stops when the change in the residual is smaller than this value.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=True,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    C,
    coef0,
    degree,
    epsilon,
    kernel,
    max_iter,
    shrinking,
    tol,
]
