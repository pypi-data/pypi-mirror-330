from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


epochs = IntegerNode(
    name="epochs",
    label="Epochs",
    description="Number of epochs to train the model.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=2,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
learning_rate = FloatNode(
    name="learning_rate",
    label="Learning Rate",
    description="Learning rate for the optimizer.",
    domain=FloatSet.closed(1e-06, 0.0001),
    enabled=False,
    default_value=5e-05,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_length = IntegerNode(
    name="max_length",
    label="Max Length",
    description="Maximum length of the input sequence.",
    domain=IntegerSet.closed(32, 512),
    enabled=False,
    default_value=64,
    constraint=False,
    constraintInformation=None,
)
model = CategoricalNode(
    name="model",
    label="Transformer Model Name",
    description="Name of the transformer model.",
    domain=CategoricalSet(
        categories={
            "bert-base-uncased",
            "roberta-base",
            "distilbert-base-cased",
            "bert-base-cased",
            "albert-base-v2",
            "distilbert-base-uncased",
        }
    ),
    enabled=False,
    default_value="bert-base-cased",
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    epochs,
    learning_rate,
    max_length,
    model,
]
