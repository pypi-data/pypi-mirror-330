from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


batch_size = IntegerNode(
    name="batch_size",
    label="Batch Size",
    description="The batch size parameter determines the number of training examples used to calculate the gradient update in each iteration of the optimization process, influencing both the training speed and the model's generalization performance.",
    domain=IntegerSet.closedopen(1, 129),
    enabled=False,
    default_value=32,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
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
lr_scheduler_type = CategoricalNode(
    name="lr_scheduler_type",
    label="Learning Rate Scheduler",
    description="Specifies the type of learning rate scheduler used during training, controlling how the learning rate is adjusted over time to improve model convergence and performance.",
    domain=CategoricalSet(
        categories={
            "cosine",
            "linear",
            "cosine_with_restarts",
            "constant",
            "polynomial",
            "constant_with_warmup",
        }
    ),
    enabled=False,
    default_value="linear",
    constraint=False,
    constraintInformation=None,
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
            "deepmind/language-perceiver",
            "gpt2",
            "distilbert-base-uncased",
            "facebook/bart-base",
            "albert-base-v2",
            "google/electra-base-discriminator",
        }
    ),
    enabled=False,
    default_value="bert-base-uncased",
    constraint=False,
    constraintInformation=None,
)
warmup_ratio = FloatNode(
    name="warmup_ratio",
    label="Warmup Ratio",
    description="Determines the proportion of total training steps dedicated to the warm-up phase, during which the learning rate gradually increases to its initial value to ensure stable training.",
    domain=FloatSet.closed(0.0, 1.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)

parameter_nodes = [
    batch_size,
    epochs,
    learning_rate,
    lr_scheduler_type,
    max_length,
    model,
    warmup_ratio,
]
