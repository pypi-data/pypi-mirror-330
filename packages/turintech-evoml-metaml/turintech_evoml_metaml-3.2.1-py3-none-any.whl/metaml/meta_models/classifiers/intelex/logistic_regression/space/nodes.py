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
    description="Inverse of regularization strength (positive float); smaller values indicate stronger regularization, which helps prevent overfitting.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
class_weight = CategoricalNode(
    name="class_weight",
    label="Class weight",
    description="Enables control over the weight of different the classes in your training dataset, which can be beneficial when working with imbalanced data. If set to None, all classes are given equal weight. If set to balanced, the class weights are adjusted proportionally to their frequencies in the input data.",
    domain=CategoricalSet(categories={"balanced", "None"}),
    enabled=False,
    default_value="None",
    constraint=False,
    constraintInformation=None,
)
dual = CategoricalNode(
    name="dual",
    label="Dual",
    description="Boolean indicating whether to use the dual or primal formulation of the optimization problem.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=True,
    constraintInformation="When dual is True, penalty must be l2, and solver must be liblinear.",
)
fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Calculate Intercept",
    description="Boolean indicating whether to calculate the model's intercept; if False, data is expected to be centered and no intercept is used.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
intercept_scaling = FloatNode(
    name="intercept_scaling",
    label="Intercept scaling",
    description="Applicable when using 'liblinear' solver and 'fit_intercept' is True; adds a synthetic feature with a constant value equal to intercept_scaling to the instance vector.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
l1_ratio = MixedNode(
    name="l1_ratio",
    label="L1 ratio",
    description="Elastic-Net mixing parameter (0 <= l1_ratio <= 1); controls the balance between L1 and L2 regularization.",
    domain=MixedSet(
        float_set=FloatSet.closed(0.0, 1.0),
        integer_set=IntegerSet(),
        categorical_set=CategoricalSet(categories={"None"}),
    ),
    enabled=True,
    default_value="None",
    constraint=True,
    constraintInformation="When penalty is elasticnet, l1_ratio must be between 0 and 1.",
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="Maximum number of iterations for the solver to converge.",
    domain=IntegerSet.closedopen(50, 201),
    enabled=True,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
multi_class = CategoricalNode(
    name="multi_class",
    label="Multi_class",
    description="Strategy for handling multi-class problems; 'ovr' fits a binary problem for each label, while 'multinomial' minimizes the multinomial loss across the entire probability distribution.",
    domain=CategoricalSet(categories={"auto", "ovr", "multinomial"}),
    enabled=False,
    default_value="auto",
    constraint=True,
    constraintInformation="When solver is liblinear, multi_class must be auto or ovr.",
)
penalty = CategoricalNode(
    name="penalty",
    label="Penalty",
    description="Norm of the regularization penalty (e.g., 'l1', 'l2', 'elasticnet').",
    domain=CategoricalSet(categories={"None", "l1", "elasticnet", "l2"}),
    enabled=True,
    default_value="l2",
    constraint=True,
    constraintInformation="When dual is True, penalty must be l2. When penalty is none, solver must be one of (newton-cg, lbfgs, sag, saga). When penalty is l1, solver must be saga or liblinear. When penalty is elasticnet, solver must be saga. When penalty is elasticnet, l1_ratio must be between 0 and 1.",
)
solver = CategoricalNode(
    name="solver",
    label="Solver",
    description="Algorithm used to solve the optimization problem (e.g., 'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga').",
    domain=CategoricalSet(categories={"sag", "newton-cg", "lbfgs", "liblinear", "saga"}),
    enabled=True,
    default_value="lbfgs",
    constraint=True,
    constraintInformation="When dual is True, solver must be liblinear. When penalty is none, solver must be one of (newton-cg, lbfgs, sag, saga). When penalty is l1, solver must be saga or liblinear. When penalty is elasticnet, solver must be saga. When solver is liblinear, multi_class must be auto or ovr.",
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Tolerance for stopping criterion; solver converges when the residual's maximum norm is below this value.",
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
    l1_ratio,
    max_iter,
    multi_class,
    penalty,
    solver,
    tol,
]
