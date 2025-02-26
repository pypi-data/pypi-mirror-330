from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


C = FloatNode(
    name="C",
    label="C",
    description="Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.",
    domain=FloatSet.closed(0.1, 25.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
class_weight = CategoricalNode(
    name="class_weight",
    label="Class weight",
    description="Weights associated with classes in the form {class_label: weight}. If not given, all classes are supposed to have weight one. The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y)).",
    domain=CategoricalSet(categories={"balanced", "None"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
dual = CategoricalNode(
    name="dual",
    label="Dual",
    description="Select the algorithm to either solve the dual or primal optimization problem. Prefer dual=False when n_samples > n_features.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=True,
    constraintInformation="When dual is True, penalty must be l2. When dual is False, loss must be squared_hinge.",
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
intercept_scaling = FloatNode(
    name="intercept_scaling",
    label="Intercept scaling",
    description="Useful only when the solver 'liblinear' is used and self.fit_intercept is set to True. In this case, x becomes [x, self.intercept_scaling], i.e. a “synthetic” feature with constant value equal to intercept_scaling is appended to the instance vector. The intercept becomes intercept_scaling * synthetic_feature_weight.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="Specifies the loss function. inge is the standard SVM loss while squared_hingeis the square of the hinge loss.",
    domain=CategoricalSet(categories={"hinge", "squared_hinge"}),
    enabled=False,
    default_value="squared_hinge",
    constraint=True,
    constraintInformation="When dual is True, penalty must be l2. When dual is False, loss must be squared_hinge.",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="    Maximum number of iterations taken for the solvers to converge.",
    domain=IntegerSet.closedopen(500, 2001),
    enabled=True,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
multi_class = CategoricalNode(
    name="multi_class",
    label="Multi-class",
    description="Determines the multi-class strategy if y contains more than two classes.",
    domain=CategoricalSet(categories={"crammer_singer", "ovr"}),
    enabled=False,
    default_value="ovr",
    constraint=False,
    constraintInformation=None,
)
penalty = CategoricalNode(
    name="penalty",
    label="Penalty",
    description="Specifies the norm used in the penalization. The l2 penalty is the standard used in SVC. The l1 leads to coef_vectors that are sparse.",
    domain=CategoricalSet(categories={"l1", "l2"}),
    enabled=False,
    default_value="l2",
    constraint=True,
    constraintInformation="When dual is True, penalty must be l2.",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Maximum norm of the residual.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=True,
    default_value=0.0001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    C,
    class_weight,
    dual,
    fit_intercept,
    intercept_scaling,
    loss,
    max_iter,
    multi_class,
    penalty,
    tol,
]
