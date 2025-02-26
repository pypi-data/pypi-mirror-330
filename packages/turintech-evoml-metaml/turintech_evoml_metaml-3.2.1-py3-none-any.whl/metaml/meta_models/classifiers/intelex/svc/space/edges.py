from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet
from .nodes import decision_function_shape, break_ties

mapping_decision_function_shape_to_break_ties = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"ovo"}),
            target=CategoricalSet(categories={False}),
        ),
        MappingItem(
            source=CategoricalSet(categories={"ovr"}),
            target=CategoricalSet(categories={True, False}),
        ),
    ]
)

constraint_decision_function_shape_to_break_ties = ConstraintEdge(
    source=decision_function_shape.name,
    target=break_ties.name,
    mapping=mapping_decision_function_shape_to_break_ties,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_decision_function_shape_to_break_ties,
]
