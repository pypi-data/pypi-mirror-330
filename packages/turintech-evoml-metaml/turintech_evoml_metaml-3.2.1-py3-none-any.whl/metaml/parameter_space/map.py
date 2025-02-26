from pydantic import BaseModel, validator
from typing import List, Dict, Generic, TypeVar, Type, NamedTuple


from metaml.parameter_space.set import MixedSet, IntegerSet, FloatSet, CategoricalSet


SourceDomainType = TypeVar("SourceDomainType", CategoricalSet, FloatSet, IntegerSet, MixedSet)
TargetDomainType = TypeVar("TargetDomainType", CategoricalSet, FloatSet, IntegerSet, MixedSet)


class MappingItem(BaseModel, Generic[SourceDomainType, TargetDomainType]):
    """
    Represents a pair of source and target sets, all of whose elements are compatible.

    Attributes
    ----------
        source (SourceDomainType): The source domain of the mapping.
        target (TargetDomainType): The target domain of the mapping.
    """

    source: SourceDomainType
    target: TargetDomainType

    class Config:
        extra = "forbid"


class Mapping(BaseModel, Generic[SourceDomainType, TargetDomainType]):
    """Represents a mapping between two domains. Can be used to represent constraints. Mappings consist of a list of
    pairs of compatible source and target sets."""

    items: List[MappingItem]

    # Validation
    @validator("items")
    def validate_source_types(cls, items: List[MappingItem]):
        """Validates that all source values in the mapping are of the same type."""
        if len(items) > 1:
            source_type = type(items[0].source)
            if not all(isinstance(item.source, source_type) for item in items):
                raise TypeError("All source values in MappingItem must be of the same type.")
        return items

    @validator("items")
    def validate_target_types(cls, items: List[MappingItem]):
        """Validates that all target values in the mapping are of the same type."""
        if len(items) > 1:
            target_type = type(items[0].target)
            if not all(isinstance(item.target, target_type) for item in items):
                raise TypeError("All target values in MappingItem must be of the same type.")
        return items

    @validator("items")
    def validate_mapping_not_empty(cls, items: List[MappingItem]):
        """Validates that the mapping is not empty."""
        if not items:
            raise ValueError("The mapping item list cannot be empty.")
        return items

    # Construction
    @classmethod
    def from_dict(cls, mapping_dict: Dict[SourceDomainType, TargetDomainType]) -> "Mapping":
        """Class constructor to build a mapping from a dictionary."""
        mapping_items = [MappingItem(source=k, target=v) for k, v in mapping_dict.items()]
        return cls(items=mapping_items)

    # Properties
    @property
    def source_type(self) -> Type[SourceDomainType]:
        """Returns the type of the source domain."""
        return type(self.items[0].source)

    @property
    def target_type(self) -> Type[TargetDomainType]:
        """Returns the type of the target domain."""
        return type(self.items[0].target)

    # Mapping functions
    def forward(self, source: SourceDomainType) -> TargetDomainType:
        """Computes the union of all elements in the target domain that are compatible with any element of the provided
        source set."""
        if not isinstance(source, self.source_type):
            source = self.source_type.unit(source)

        compatible_targets = self.target_type()
        for mapping_item in self.items:
            if source.intersection(mapping_item.source):
                compatible_targets = compatible_targets.union(mapping_item.target)

        return compatible_targets

    def backward(self, target_set: TargetDomainType) -> SourceDomainType:
        """Computes the union of all elements in the source domain that are compatible with any element of the provided
        target set."""
        compatible_sources = self.source_type()
        for mapping_item in self.items:
            if target_set.intersection(mapping_item.target):
                compatible_sources = compatible_sources.union(mapping_item.source)

        return compatible_sources


class ConstraintEdge(NamedTuple):
    """Tuple representing information to add a constraint edge to a parameter graph."""

    source: str
    target: str
    mapping: Mapping
