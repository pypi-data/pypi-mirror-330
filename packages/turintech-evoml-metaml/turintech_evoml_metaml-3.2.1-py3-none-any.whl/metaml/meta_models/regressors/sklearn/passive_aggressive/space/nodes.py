from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


C = FloatNode(
    name="C",
    label="C",
    description="Controls the inverse of regularization strength, with smaller values resulting in stronger regularization. Regularization helps prevent overfitting by penalizing large weights.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
early_stopping = CategoricalNode(
    name="early_stopping",
    label="Early stopping",
    description="Determines if early stopping should be used to halt training when the validation score is not improving, preventing overfitting and reducing training time.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=False,
    constraint=False,
    constraintInformation=None,
)
epsilon = FloatNode(
    name="epsilon",
    label="Epsilon",
    description="Determines the threshold for the loss function, below which the model will not be updated. This balances the model's sensitivity to small errors and its robustness to noise.",
    domain=FloatSet.closed(0.0001, 1.0),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Calculate Intercept",
    description="Indicates if an intercept should be calculated for the model.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="Specifies the loss function to be optimized during training.",
    domain=CategoricalSet(categories={"epsilon_insensitive", "squared_epsilon_insensitive"}),
    enabled=True,
    default_value="epsilon_insensitive",
    constraint=False,
    constraintInformation=None,
)
max_iter = IntegerNode(
    name="max_iter",
    label="Maximum number of iterations",
    description="Sets the maximum number of iterations for the solver to converge, controlling the maximum training time.",
    domain=IntegerSet.closedopen(0, 2001),
    enabled=True,
    default_value=1000,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_iter_no_change = IntegerNode(
    name="n_iter_no_change",
    label="Maximum number of iterations with no change",
    description="Defines the maximum number of epochs without improvement in the validation score before stopping. Only effective when the solver is 'sgd' or 'adam'.",
    domain=IntegerSet.closedopen(2, 11),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
shuffle = CategoricalNode(
    name="shuffle",
    label="Shuffle",
    description="Determines if samples should be shuffled in each iteration, which can help avoid getting stuck in local minima.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
tol = FloatNode(
    name="tol",
    label="Tolerance",
    description="Controls the stopping criterion in iterative algorithms, specifying the minimum improvement in the objective function or loss between consecutive iterations required for the algorithm to continue training.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.001,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
validation_fraction = FloatNode(
    name="validation_fraction",
    label="Validation fraction",
    description="Specifies the proportion of training data to be set aside as a validation set for early stopping.",
    domain=FloatSet.closed(0.0, 0.9999),
    enabled=False,
    default_value=0.1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    C,
    early_stopping,
    epsilon,
    fit_intercept,
    loss,
    max_iter,
    n_iter_no_change,
    shuffle,
    tol,
    validation_fraction,
]
