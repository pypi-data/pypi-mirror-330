from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet
from .nodes import dual, penalty, loss

mapping_dual_to_penalty = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"l2"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"l1", "l2"}),
        ),
    ]
)

constraint_dual_to_penalty = ConstraintEdge(
    source=dual.name,
    target=penalty.name,
    mapping=mapping_dual_to_penalty,
)

mapping_dual_to_loss = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"squared_hinge", "hinge"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"squared_hinge"}),
        ),
    ]
)

constraint_dual_to_loss = ConstraintEdge(
    source=dual.name,
    target=loss.name,
    mapping=mapping_dual_to_loss,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_dual_to_penalty,
    constraint_dual_to_loss,
]
