from metaml.parameter_space.node import CategoricalNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, IntegerSet


lags = IntegerNode(
    name="lags",
    label="Lags",
    description="The number of lagged observations of the target series to use as input features.",
    domain=IntegerSet.closedopen(1, 13),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
lags_past_covariates = IntegerNode(
    name="lags_past_covariates",
    label="Last Past Covariates",
    description="The number of lagged past covariates to use as input features.",
    domain=IntegerSet.closedopen(1, 13),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
output_chunk_length = IntegerNode(
    name="output_chunk_length",
    label="Output Chunk Length",
    description="Specifies the number of time steps forecasted at once, with these forecasts then used as input for generating the next set of predictions in an autoregressive manner when forecasting over long horizons.",
    domain=IntegerSet.closedopen(1, 21),
    enabled=False,
    default_value=5,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Fit Intercept",
    description="Whether or not to fit the intercept term.",
    domain=CategoricalSet(categories={False, True}),
    enabled=False,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)


parameter_nodes = [
    lags,
    lags_past_covariates,
    output_chunk_length,
    fit_intercept,
]
