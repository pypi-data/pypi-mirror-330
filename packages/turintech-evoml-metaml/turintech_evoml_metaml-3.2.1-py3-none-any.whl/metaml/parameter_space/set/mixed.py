from __future__ import annotations
from typing import Any


from metaml.parameter_space.set import FloatSet, IntegerSet, CategoricalSet, BaseSet


class MixedSet(BaseSet):
    """A class representing a mixed set, can contain float, integer and categorical elements."""

    float_set: FloatSet = FloatSet()
    integer_set: IntegerSet = IntegerSet()
    categorical_set: CategoricalSet = CategoricalSet()

    # Constructors
    @classmethod
    def unit(cls, element: Any) -> MixedSet:
        """Return a MixedSet containing only the given element."""
        if isinstance(element, int):
            return cls(integer_set=IntegerSet.unit(element))
        elif isinstance(element, float):
            return cls(float_set=FloatSet.unit(element))
        return cls(categorical_set=CategoricalSet.unit(element))

    # Set operations
    def intersection(self, other: MixedSet) -> MixedSet:
        """Perform an intersection between two MixedSets."""
        if not isinstance(other, MixedSet):
            raise TypeError(f"Cannot intersect MixedSet with {type(other)}.")
        return MixedSet(
            float_set=self.float_set.intersection(other.float_set),
            integer_set=self.integer_set.intersection(other.integer_set),
            categorical_set=self.categorical_set.intersection(other.categorical_set),
        )

    def union(self, other: MixedSet) -> MixedSet:
        """Perform a union between two MixedSets."""
        if not isinstance(other, MixedSet):
            raise TypeError(f"Cannot take the union of a MixedSet and {type(other)}.")
        return MixedSet(
            float_set=self.float_set.union(other.float_set),
            integer_set=self.integer_set.union(other.integer_set),
            categorical_set=self.categorical_set.union(other.categorical_set),
        )

    def difference(self, other: MixedSet) -> MixedSet:
        """Perform a difference between two MixedSets."""
        if not isinstance(other, MixedSet):
            raise TypeError(f"Cannot take the difference of a MixedSet and {type(other)}.")
        return MixedSet(
            float_set=self.float_set.difference(other.float_set),
            integer_set=self.integer_set.difference(other.integer_set),
            categorical_set=self.categorical_set.difference(other.categorical_set),
        )

    def sample(self):
        raise NotImplementedError("The sample method for MixedSet is not implemented yet.")

    # Properties
    @property
    def is_empty(self) -> bool:
        """Return True if the set is empty, False otherwise."""
        return self.float_set.is_empty and self.integer_set.is_empty and self.categorical_set.is_empty

    @property
    def is_singleton(self) -> bool:
        """
        Property to check if a MixedSet is a singleton.

        A MixedSet is considered a singleton if exactly one of its component sets (float_set, integer_set,
        categorical_set) is a singleton and the others are empty.

        Returns:
            bool: True if the MixedSet is a singleton, False otherwise.
        """
        singleton_sets = sum(
            int(set_.is_singleton) for set_ in [self.float_set, self.integer_set, self.categorical_set]
        )
        empty_sets = sum(int(set_.is_empty) for set_ in [self.float_set, self.integer_set, self.categorical_set])

        return singleton_sets == 1 and empty_sets == 2

    @property
    def value(self) -> Any:
        """
        Property to get the value of a MixedSet.

        The value is the value of the singleton component if the MixedSet is a singleton.
        Raises a ValueError if the MixedSet is not a singleton.

        Returns:
            Any: The value of the singleton component.
        Raises:
            ValueError: If the MixedSet is not a singleton.
        """
        if not self.is_singleton:
            raise ValueError("Cannot get the value of a non-singleton MixedSet.")

        if self.float_set.is_singleton:
            return self.float_set.value
        elif self.integer_set.is_singleton:
            return self.integer_set.value
        elif self.categorical_set.is_singleton:
            return self.categorical_set.value
        raise ValueError(f"Unexpected state: {self} is a singleton but no component set is a singleton.")

    # Other special methods
    def __hash__(self):
        """Return a hash of the MixedSet."""
        return hash((self.float_set, self.integer_set, self.categorical_set))
