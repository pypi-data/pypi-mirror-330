from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


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
eta = FloatNode(
    name="eta",
    label="Eta",
    description="Decrease factor for line-search procedure.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
gamma = FloatNode(
    name="gamma",
    label="Gamma",
    description="Gamma coefficient in the loss 'smooth_hinge'.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
l1_ratio = FloatNode(
    name="l1_ratio",
    label="L1 ratio",
    description="The L1 ratio parameter represents the trade-off between the L1 and L2 regularization terms in the objective function. A value of 0 indicates L2 regularization only, while a value of 1 indicates L1 regularization only. Values between 0 and 1 apply a mix of both L1 and L2 regularization, which can be advantageous for capturing different types of feature importance while preventing overfitting.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
loss = CategoricalNode(
    name="loss",
    label="Loss",
    description="The loss function to be used.",
    domain=CategoricalSet(
        categories={
            "modified_huber",
            "squared",
            "log",
            "squared_hinge",
            "hinge",
            "perceptron",
            "smooth_hinge",
        }
    ),
    enabled=True,
    default_value="hinge",
    constraint=False,
    constraintInformation=None,
)
n_iter = IntegerNode(
    name="n_iter",
    label="Number of iterations",
    description="This parameter specifies the maximum number of iterations the optimization algorithm will run to converge to a solution. Each iteration involves a complete pass over the training data. Setting this to a low value may speed up training but could result in suboptimal performance. Conversely, a higher value may allow the model to converge to a better solution but at the cost of increased computational time.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
shuffle = CategoricalNode(
    name="shuffle",
    label="Shuffle",
    description="Whether to shuffle data.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    alpha,
    eta,
    gamma,
    l1_ratio,
    loss,
    n_iter,
    shuffle,
]
