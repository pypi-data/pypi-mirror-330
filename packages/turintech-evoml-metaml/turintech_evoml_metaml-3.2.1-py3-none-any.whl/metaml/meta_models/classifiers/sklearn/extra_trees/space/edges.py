from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import FloatSet, CategoricalSet, MixedSet
from .nodes import bootstrap, max_samples


mapping_bootstrap_to_max_samples = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=MixedSet(
                float_set=FloatSet.closed(0.0001, 1.0),
                categorical_set=CategoricalSet(categories={"None"}),
            ),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
    ]
)

constraint_bootstrap_to_max_samples = ConstraintEdge(
    source=bootstrap.name,
    target=max_samples.name,
    mapping=mapping_bootstrap_to_max_samples,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_bootstrap_to_max_samples,
]
