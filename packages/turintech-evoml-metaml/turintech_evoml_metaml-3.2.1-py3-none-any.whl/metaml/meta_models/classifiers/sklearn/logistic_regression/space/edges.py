from typing import List


from metaml.parameter_space.graph import ConstraintEdge
from metaml.parameter_space.map import Mapping, MappingItem
from metaml.parameter_space.set import CategoricalSet, FloatSet, MixedSet
from .nodes import penalty, solver, l1_ratio, multi_class, dual


mapping_penalty_to_l1_ratio = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"l1"}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={"l1", "l2", "None"}),
            target=MixedSet(categorical_set=CategoricalSet(categories={"None"})),
        ),
        MappingItem(
            source=CategoricalSet(categories={"elasticnet"}),
            target=MixedSet(float_set=FloatSet.closed(0.0, 1.0)),
        ),
    ]
)
constraint_penalty_to_l1_ratio = ConstraintEdge(
    source=penalty.name,
    target=l1_ratio.name,
    mapping=mapping_penalty_to_l1_ratio,
)


mapping_penalty_to_solver = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"l1"}),
            target=CategoricalSet(categories={"saga", "liblinear"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={"l2"}),
            target=CategoricalSet(categories={"saga", "newton-cg", "lbfgs", "sag", "liblinear"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={"elasticnet"}),
            target=CategoricalSet(categories={"saga"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={"None"}),
            target=CategoricalSet(categories={"saga", "newton-cg", "lbfgs", "sag"}),
        ),
    ]
)
constraint_penalty_to_solver = ConstraintEdge(
    source=penalty.name,
    target=solver.name,
    mapping=mapping_penalty_to_solver,
)


mapping_dual_to_solver = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={True}),
            target=CategoricalSet(categories={"liblinear"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={False}),
            target=CategoricalSet(categories={"saga", "newton-cg", "lbfgs", "sag", "liblinear"}),
        ),
    ]
)
constraint_dual_to_solver = ConstraintEdge(
    source=dual.name,
    target=solver.name,
    mapping=mapping_dual_to_solver,
)


mapping_multi_class_to_solver = Mapping(
    items=[
        MappingItem(
            source=CategoricalSet(categories={"ovr", "auto"}),
            target=CategoricalSet(categories={"saga", "newton-cg", "lbfgs", "sag", "liblinear"}),
        ),
        MappingItem(
            source=CategoricalSet(categories={"multinomial"}),
            target=CategoricalSet(categories={"saga", "newton-cg", "lbfgs", "sag"}),
        ),
    ]
)
constraint_multi_class_to_solver = ConstraintEdge(
    source=multi_class.name,
    target=solver.name,
    mapping=mapping_multi_class_to_solver,
)


constraint_edges: List[ConstraintEdge] = [
    constraint_penalty_to_l1_ratio,
    constraint_penalty_to_solver,
    constraint_dual_to_solver,
    constraint_multi_class_to_solver,
]
