from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


activation = CategoricalNode(
    name="activation",
    label="Activation Function",
    description="The activation function applied in the N-BEATS forecaster neural network layers.",
    domain=CategoricalSet(
        categories={
            "PReLU",
            "Tanh",
            "ReLU",
            "RReLU",
            "SELU",
            "Softplus",
            "LeakyReLU",
            "Sigmoid",
        }
    ),
    enabled=False,
    default_value="ReLU",
    constraint=False,
    constraintInformation=None,
)
dropout = FloatNode(
    name="dropout",
    label="Dropout Rate",
    description="The dropout rate applied to the N-BEATS forecaster neural network layers to prevent overfitting.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
expansion_coefficient_dim = IntegerNode(
    name="expansion_coefficient_dim",
    label="Expansion Coefficient Dimension",
    description="The dimension of the expansion coefficients in the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 101),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_epochs = IntegerNode(
    name="n_epochs",
    label="Number of Epochs",
    description="The number of times the N-BEATS forecaster model is trained on the entire dataset.",
    domain=IntegerSet.closedopen(1, 501),
    enabled=False,
    default_value=10,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
generic_architecture = CategoricalNode(
    name="generic_architecture",
    label="Generic Architecture",
    description="Use a generic architecture for the N-BEATS forecaster model instead of a specialized one.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)
input_chunk_length = IntegerNode(
    name="input_chunk_length",
    label="Input Chunk Length",
    description="The length of the input time series chunks used by the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 101),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
layer_widths = IntegerNode(
    name="layer_widths",
    label="Layer Widths",
    description="The width of the neural network layers in the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 1025),
    enabled=False,
    default_value=256,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
num_stacks = IntegerNode(
    name="num_stacks",
    label="Number of Stacks",
    description="The number of stacks in the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 101),
    enabled=False,
    default_value=30,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
num_blocks = IntegerNode(
    name="num_blocks",
    label="Number of Blocks",
    description="The number of blocks per stack in the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
num_layers = IntegerNode(
    name="num_layers",
    label="Number of Layers",
    description="The number of layers per block in the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=4,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
output_chunk_length = IntegerNode(
    name="output_chunk_length",
    label="Output Chunk Length",
    description="The length of the output time series chunks produced by the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 101),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
trend_polynomial_degree = IntegerNode(
    name="trend_polynomial_degree",
    label="Trend Polynomial Degree",
    description="The degree of the polynomial used to model the trend component in the N-BEATS forecaster model.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=2,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    activation,
    dropout,
    expansion_coefficient_dim,
    n_epochs,
    generic_architecture,
    input_chunk_length,
    layer_widths,
    num_stacks,
    num_blocks,
    num_layers,
    output_chunk_length,
    trend_polynomial_degree,
]
