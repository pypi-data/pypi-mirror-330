from __future__ import annotations
from typing import Any, Optional, Set, List, Union
from pydantic import StrictBool, StrictStr
import random


from metaml.parameter_space.set.base import BaseSet


class CategoricalSet(BaseSet):
    """Represents a set of strings, booleans or the None special constant

    Attributes
    ----------
    categories : Set[Union[StrictBool, StrictStr, None]]
        The set of categories that make up the set. Default is an empty set.
    """

    categories: Set[Union[StrictBool, StrictStr, None]] = set()

    # Constructors
    def __init__(self, categories: Optional[Union[Set, List]] = None) -> None:
        """Initializes a CategoricalSet. This method allows categories to be treated as a positional argument."""
        categories = set() if categories is None else set(categories)
        super().__init__(categories=categories)

    @classmethod
    def unit(cls, category: Any) -> CategoricalSet:
        """Class method that returns a new CategoricalSet containing only 'category'."""
        return cls([category])

    @classmethod
    def empty(cls) -> CategoricalSet:
        """Class method that returns a new empty CategoricalSet."""
        return cls()

    # Set operations
    def intersection(self, other: CategoricalSet) -> CategoricalSet:
        """Returns a new CategoricalSet that is the intersection of this set and 'other'."""
        if not isinstance(other, CategoricalSet):
            raise TypeError(f"Cannot take the difference of a CategoricalSet and {type(other)}.")
        return CategoricalSet(self.categories.intersection(other.categories))

    def union(self, other: CategoricalSet) -> CategoricalSet:
        """Returns a new CategoricalSet that is the union of this set and 'other'."""
        if not isinstance(other, CategoricalSet):
            raise TypeError(f"Cannot take the union of a CategoricalSet and {type(other)}.")
        return CategoricalSet(self.categories.union(other.categories))

    def difference(self, other: CategoricalSet) -> CategoricalSet:
        """Returns a new CategoricalSet that is the difference of this set and 'other'."""
        if not isinstance(other, CategoricalSet):
            raise TypeError(f"Cannot take the difference of a CategoricalSet and {type(other)}.")
        return CategoricalSet(self.categories.difference(other.categories))

    def sample(self) -> CategoricalSet:
        """Take a sample from the set."""
        if self.is_empty:
            raise ValueError(f"Cannot sample from an empty set: {self}.")
        sample_value = random.choice(list(self.categories))
        return CategoricalSet.unit(sample_value)

    # Properties
    @property
    def is_empty(self) -> bool:
        """Returns True if this CategoricalSet is empty, False otherwise."""
        return not self.categories

    @property
    def is_singleton(self) -> bool:
        """Returns True if this CategoricalSet contains exactly one element, False otherwise."""
        return len(self.categories) == 1

    @property
    def value(self) -> Union[StrictBool, StrictStr, None]:
        """Returns the single element of this CategoricalSet if it is a singleton, otherwise raises a ValueError."""
        if self.is_singleton:
            return next(iter(self.categories))
        raise ValueError("Cannot get value of a non-singleton set.")

    # Other special methods
    def __hash__(self) -> int:
        """Returns a hash of the CategoricalSet data."""
        return hash(frozenset(self.categories))
