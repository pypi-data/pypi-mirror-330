from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseSet(ABC, BaseModel):
    """Abstract base class for sets."""

    class Config:
        extra = "forbid"

    # Set operations
    @abstractmethod
    def intersection(self, other: BaseSet) -> BaseSet:
        """Returns a new set that is the intersection of this set and 'other'."""
        ...

    @abstractmethod
    def union(self, other: BaseSet) -> BaseSet:
        """Returns a new set that is the union of this set and 'other'."""
        ...

    @abstractmethod
    def difference(self, other: BaseSet) -> BaseSet:
        """Returns a new set that contains all elements of this set that are not in 'other'."""
        ...

    def __or__(self, other) -> BaseSet:
        """Implements the "|" operator as the union of two sets, which is the same as taking the union."""
        return self.union(other)

    def __contains__(self, value: Any) -> bool:
        """Returns True if 'element' is in the set, and False otherwise."""
        return (
            self.intersection(value) == value
            if isinstance(value, self.__class__)
            else self.unit(value).intersection(self) == self.unit(value)
        )

    # Unit set constructor
    @classmethod
    @abstractmethod
    def unit(cls, element: Any) -> BaseSet:
        """Class method that returns a new unit (singleton) set containing only 'element'."""
        ...

    # Special methods
    @abstractmethod
    def __hash__(self) -> int:
        """Returns a hash of the set."""
        ...

    def __bool__(self) -> bool:
        """Returns False if the set is empty and True otherwise."""
        return not self.is_empty

    # Other methods
    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the set is empty and False otherwise."""
        ...

    @abstractmethod
    def sample(self) -> BaseSet:
        """Returns a random element of the set."""
        ...
