from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet
from .nodes import multiclass, penalty, loss

mapping_multiclass_to_penalty = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"l1/l2"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"l1/l2", "l2", "l1"}),
        ),
    ]
)

constraint_multiclass_to_penalty = ConstraintEdge(
    source=multiclass.name,
    target=penalty.name,
    mapping=mapping_multiclass_to_penalty,
)

mapping_multiclass_to_loss = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"squared_hinge", "log"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"squared_hinge", "log", "modified_huber", "squared"}),
        ),
    ]
)

constraint_multiclass_to_loss = ConstraintEdge(
    source=multiclass.name,
    target=loss.name,
    mapping=mapping_multiclass_to_loss,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_multiclass_to_penalty,
    constraint_multiclass_to_loss,
]
