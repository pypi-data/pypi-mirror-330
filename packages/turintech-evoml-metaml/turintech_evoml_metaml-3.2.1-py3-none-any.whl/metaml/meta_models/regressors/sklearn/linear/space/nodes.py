from metaml.parameter_space.node import CategoricalNode
from metaml.parameter_space.set import CategoricalSet


fit_intercept = CategoricalNode(
    name="fit_intercept",
    label="Calculate Intercept",
    description="Determines whether to include an intercept term in the linear regression model. If set to True, the model will calculate the intercept; if set to False, the model assumes that the data is centered and will not use an intercept in calculations.",
    domain=CategoricalSet(categories={False, True}),
    enabled=True,
    default_value=True,
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    fit_intercept,
]
