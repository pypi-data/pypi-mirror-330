from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet
from .nodes import multiclass, loss


mapping_multiclass_to_loss = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"squared_hinge"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"squared_hinge", "log", "log_margin"}),
        ),
    ]
)

constraint_multiclass_to_loss = ConstraintEdge(
    source=multiclass.name,
    target=loss.name,
    mapping=mapping_multiclass_to_loss,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_multiclass_to_loss,
]
