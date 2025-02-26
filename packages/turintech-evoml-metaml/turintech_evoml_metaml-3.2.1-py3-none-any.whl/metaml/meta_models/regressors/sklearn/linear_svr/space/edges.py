from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet
from .nodes import dual, loss


mapping_dual_to_loss = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"squared_epsilon_insensitive"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"epsilon_insensitive", "squared_epsilon_insensitive"}),
        ),
    ]
)

constraint_dual_to_loss = ConstraintEdge(
    source=dual.name,
    target=loss.name,
    mapping=mapping_dual_to_loss,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_dual_to_loss,
]
