from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet, FloatSet, MixedSet
from .nodes import (
    boost_from_average,
    model_shrink_rate,
    boosting_type,
    approx_on_full_history,
    bootstrap_type,
    bagging_temperature,
    subsample,
)


mapping_boost_from_average_to_model_shrink_rate = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=MixedSet(
                float_set=FloatSet.closed(0.0, 0.999),
                categorical_set=CategoricalSet(categories={"None"}),
            ),
        ),
    ]
)

constraint_boost_from_average_to_model_shrink_rate = ConstraintEdge(
    source=boost_from_average.name,
    target=model_shrink_rate.name,
    mapping=mapping_boost_from_average_to_model_shrink_rate,
)

mapping_boosting_type_to_approx_on_full_history = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"Plain", "None"}),
            target=CategoricalSet(categories={False}),
        ),
        MappingItem(
            source=CategoricalSet(categories={"Ordered"}),
            target=CategoricalSet(categories={True, False}),
        ),
    ]
)

constraint_boosting_type_to_approx_on_full_history = ConstraintEdge(
    source=boosting_type.name,
    target=approx_on_full_history.name,
    mapping=mapping_boosting_type_to_approx_on_full_history,
)

mapping_bootstrap_type_to_bagging_temperature = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"Bayesian"}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={"Bernoulli"}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={"MVS"}),
            target=MixedSet(
                float_set=FloatSet.closed(0.0, 1.0),
                categorical_set=CategoricalSet(categories={"None"}),
            ),
        ),
    ]
)

constraint_bootstrap_type_to_bagging_temperature = ConstraintEdge(
    source=bootstrap_type.name,
    target=bagging_temperature.name,
    mapping=mapping_bootstrap_type_to_bagging_temperature,
)

mapping_bootstrap_type_to_subsample = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"Bayesian"}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={"Bernoulli", "MVS"}),
            target=MixedSet(
                float_set=FloatSet.closed(0.4, 1.0),
                categorical_set=CategoricalSet(categories={"None"}),
            ),
        ),
    ]
)

constraint_bootstrap_type_to_subsample = ConstraintEdge(
    source=bootstrap_type.name,
    target=subsample.name,
    mapping=mapping_bootstrap_type_to_subsample,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_boost_from_average_to_model_shrink_rate,
    constraint_boosting_type_to_approx_on_full_history,
    constraint_bootstrap_type_to_bagging_temperature,
    constraint_bootstrap_type_to_subsample,
]
