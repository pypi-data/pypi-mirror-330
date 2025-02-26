from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


C = FloatNode(
    name="C",
    label="C",
    description="Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.",
    domain=FloatSet.closed(0.001, 10.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
break_ties = CategoricalNode(
    name="break_ties",
    label="Break ties",
    description="f true, decision_function_shape='ovr', and number of classes > 2, predict will break ties according to the confidence values of decision_function; otherwise the first class among the tied classes is returned.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=True,
    constraintInformation="When decision_function_shape is ovo, break_ties must be False.",
)
class_weight = CategoricalNode(
    name="class_weight",
    label="Class weight",
    description="Sets the weights for all classes. If None, all classes are supposed to have weight one. The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y)).",
    domain=CategoricalSet(categories={"balanced", "None"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
coef0 = FloatNode(
    name="coef0",
    label="Coefficient 0",
    description="Independent term in kernel function. It is only significant in 'poly' and 'sigmoid'.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
decision_function_shape = CategoricalNode(
    name="decision_function_shape",
    label="Decision function shape",
    description="Whether to return a one-vs-rest (ovr) decision function of shape (n_samples, n_classes) as all other classifiers, or the original one-vs-one (ovo) decision function of libsvm.",
    domain=CategoricalSet(categories={"ovr", "ovo"}),
    enabled=False,
    default_value="ovr",
    constraint=True,
    constraintInformation="When decision_function_shape is ovo, break_ties must be False.",
)
degree = IntegerNode(
    name="degree",
    label="Degree",
    description="Degree of the polynomial kernel function ('poly'). Ignored by all other kernels.",
    domain=IntegerSet.closedopen(0, 11),
    enabled=False,
    default_value=3,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
gamma = CategoricalNode(
    name="gamma",
    label="Gamma",
    description="Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.",
    domain=CategoricalSet(categories={"auto", "scale"}),
    enabled=False,
    default_value="scale",
    constraint=False,
    constraintInformation=None,
)
kernel = CategoricalNode(
    name="kernel",
    label="Kernel",
    description="Specifies the kernel type to be used in the algorithm. It must be one of, 'poly', 'rbf', 'sigmoid', 'precomputed' or a callable. If none is given, 'rbf' will be used. If a callable is given it is used to precompute the kernel matrix.",
    domain=CategoricalSet(categories={"rbf", "poly", "sigmoid"}),
    enabled=True,
    default_value="rbf",
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(1, 2001),
    enabled=True,
    default_value=2000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
shrinking = CategoricalNode(
    name="shrinking",
    label="Shrinking",
    description="Whether to use the shrinking heuristic.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0001, 0.1),
    enabled=True,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    C,
    break_ties,
    class_weight,
    coef0,
    decision_function_shape,
    degree,
    gamma,
    kernel,
    max_iter,
    shrinking,
    tol,
]
