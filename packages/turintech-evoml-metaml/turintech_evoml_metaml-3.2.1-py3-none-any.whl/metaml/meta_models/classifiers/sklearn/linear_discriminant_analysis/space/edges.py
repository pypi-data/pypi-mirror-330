from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import FloatSet, CategoricalSet, MixedSet
from .nodes import solver, shrinkage

mapping_solver_to_shrinkage = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"svd"}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={"lsqr", "eigen"}),
            target=MixedSet(float_set=FloatSet.closed(0.0, 1.0)),
        ),
    ]
)

constraint_solver_to_shrinkage = ConstraintEdge(
    source=solver.name,
    target=shrinkage.name,
    mapping=mapping_solver_to_shrinkage,
)

constraint_edges: List[ConstraintEdge] = [
    constraint_solver_to_shrinkage,
]
