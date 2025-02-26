from typing import List


from metaml.parameter_space.set import IntegerSet, FloatSet, CategoricalSet
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.graph import ConstraintEdge
from .nodes import boosting_type, subsample, subsample_freq


# Constraints for "subsample"
mapping_boosting_type_to_subsample = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"rf"}),
            target=FloatSet.closedopen(0.1, 1.0),
        ),
        MappingItem(
            source=CategoricalSet(categories={"goss"}),
            target=FloatSet.unit(1.0),
        ),
        MappingItem(
            source=CategoricalSet(categories={"gbdt", "dart"}),
            target=FloatSet.closed(0.1, 1.0),
        ),
    ]
)
constraint_boosting_type_to_subsample = ConstraintEdge(
    source=boosting_type.name,
    target=subsample.name,
    mapping=mapping_boosting_type_to_subsample,
)


# Constraints for "subsample_freq"
mapping_boosting_type_to_subsample_freq = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"rf"}),
            target=IntegerSet.closedopen(1, 11),
        ),
        MappingItem(
            source=CategoricalSet(categories={"goss"}),
            target=IntegerSet.unit(0),
        ),
        MappingItem(
            source=CategoricalSet(categories={"gbdt", "dart"}),
            target=IntegerSet.closedopen(0, 11),
        ),
    ]
)
constraint_boosting_type_to_subsample_freq = ConstraintEdge(
    source=boosting_type.name,
    target=subsample_freq.name,
    mapping=mapping_boosting_type_to_subsample_freq,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_boosting_type_to_subsample,
    constraint_boosting_type_to_subsample_freq,
]
