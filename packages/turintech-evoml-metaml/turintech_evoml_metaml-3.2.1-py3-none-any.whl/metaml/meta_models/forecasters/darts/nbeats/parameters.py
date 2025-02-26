from enum import Enum
from metaml.meta_models.parameters import ParametersModel


class Activation(str, Enum):
    RELU = "ReLU"
    RRELU = "RReLU"
    PRELU = "PReLU"
    SOFTPLUS = "Softplus"
    TANH = "Tanh"
    SELU = "SELU"
    LEAKYRELU = "LeakyReLU"
    SIGMOID = "Sigmoid"


class Params(ParametersModel):
    activation: Activation = Activation.RELU
    batch_size: int = 32
    dropout: float = 0.0
    expansion_coefficient_dim: int = 5
    n_epochs: int = 10
    generic_architecture: bool = True
    input_chunk_length: int = 5
    layer_widths: int = 256
    num_stacks: int = 30
    num_blocks: int = 1
    num_layers: int = 4
    output_chunk_length: int = 5
    trend_polynomial_degree: int = 2
