from __future__ import annotations
import portion
from typing import List
from pydantic import BaseModel
from enum import Enum
import scipy.stats


from metaml.parameter_space.set.base import BaseSet


class FloatDistribution(Enum):
    """Enumeration of all supported float distributions."""

    UNIFORM = "uniform"
    LOG_UNIFORM = "log-uniform"


class FloatInterval(BaseModel):
    """Represents a real interval with float boundaries.

    Attributes
    ----------
    left : portion.Bound
        The boundary condition for the left side of the interval. Can be either OPEN or CLOSED.
    lower : float
        The lower limit of the interval.
    upper : float
        The upper limit of the interval.
    right : portion.Bound
        The boundary condition for the right side of the interval. Can be either OPEN or CLOSED.
    """

    left: portion.Bound
    lower: float
    upper: float
    right: portion.Bound

    def __hash__(self) -> int:
        return hash((self.left, self.lower, self.upper, self.right))


class FloatSet(BaseSet):
    """Represents a set of real numbers, defined as a list of intervals.

    Attributes
    ----------
    intervals : List[FloatInterval]
        The list of intervals that make up the set. Default is an empty list.
    """

    intervals: List[FloatInterval] = []

    # Constructors
    @classmethod
    def from_portion(cls, set: portion.Interval) -> FloatSet:
        """Class constructor that returns a new FloatSet from a portion.Interval."""
        intervals = []
        for atomic in set._intervals:
            left = portion.CLOSED if atomic.left.value else portion.OPEN
            right = portion.CLOSED if atomic.right.value else portion.OPEN

            intervals.append(
                FloatInterval(
                    left=left,
                    lower=atomic.lower,
                    upper=atomic.upper,
                    right=right,
                )
            )
        return cls(intervals=intervals)

    @classmethod
    def closed(cls, lower_bound: float, upper_bound: float) -> FloatSet:
        """Class constructor that returns a new FloatSet representing an interval closed on both sides."""
        return cls.from_portion(portion.closed(lower_bound, upper_bound))

    @classmethod
    def openclosed(cls, lower_bound: float, upper_bound: float) -> FloatSet:
        """Class constructor that returns a new FloatSet representing an interval open on the left and closed on the
        right."""
        return cls.from_portion(portion.openclosed(lower_bound, upper_bound))

    @classmethod
    def closedopen(cls, lower_bound: float, upper_bound: float) -> FloatSet:
        """Class constructor that returns a new FloatSet representing an interval closed on the left and open on the
        right."""
        return cls.from_portion(portion.closedopen(lower_bound, upper_bound))

    @classmethod
    def open(cls, lower_bound: float, upper_bound: float) -> FloatSet:
        """Class constructor that returns a new FloatSet representing an interval open on both sides."""
        return cls.from_portion(portion.open(lower_bound, upper_bound))

    @classmethod
    def unit(cls, number: float) -> FloatSet:
        """Class constructor that returns a new FloatSet representing a singleton set."""
        return cls.from_portion(portion.singleton(number))

    # Set operations
    def union(self, other: FloatSet) -> FloatSet:
        """Returns a new set that is the union of this set and 'other'."""
        if not isinstance(other, FloatSet):
            raise TypeError(f"Cannot take the union of a FloatSet and {type(other)}.")
        return FloatSet.from_portion(self.portion_set | other.portion_set)

    def intersection(self, other: FloatSet) -> FloatSet:
        """Returns a new set that is the intersection of this set and 'other'."""
        if not isinstance(other, FloatSet):
            raise TypeError(f"Cannot take the intersection of a FloatSet and {type(other)}.")
        return FloatSet.from_portion(self.portion_set & other.portion_set)

    def difference(self, other: FloatSet) -> FloatSet:
        """Returns a new set that is the difference of this set and 'other'."""
        if not isinstance(other, FloatSet):
            raise TypeError(f"Cannot take the difference of a FloatSet and {type(other)}.")
        return FloatSet.from_portion(self.portion_set - other.portion_set)

    def sample(self, distribution: FloatDistribution) -> FloatSet:
        """Take a sample from a given domain."""
        if self.is_empty:
            raise ValueError("Cannot sample from an empty set.")

        if not self.is_interval:
            raise NotImplementedError(f"Sampling from a disconnected set is not yet supported: {self}.")

        if distribution == FloatDistribution.UNIFORM:
            sample_value = scipy.stats.uniform.rvs(loc=self.lower_bound, scale=self.upper_bound - self.lower_bound)
        elif distribution == FloatDistribution.LOG_UNIFORM:
            sample_value = scipy.stats.loguniform.rvs(self.lower_bound, self.upper_bound)
        else:
            raise ValueError(f"Invalid distribution: {distribution}.")

        return FloatSet.unit(sample_value)

    # Properties
    @property
    def portion_set(self) -> portion.Interval:
        """Returns the portion.Interval representation of this set. Useful for set operations."""
        result = portion.empty()
        for interval_model in self.intervals:
            interval = portion.Interval.from_atomic(
                left=interval_model.left,
                lower=interval_model.lower,
                upper=interval_model.upper,
                right=interval_model.right,
            )
            result |= interval
        return result

    @property
    def is_interval(self) -> bool:
        """Returns True if this set is an interval, False otherwise."""
        return len(self.portion_set._intervals) == 1

    @property
    def lower_bound(self) -> float:
        """Returns the lower bound of this set."""
        return self.portion_set.lower

    @property
    def upper_bound(self) -> float:
        """Returns the upper bound of this set."""
        return self.portion_set.upper

    @property
    def is_empty(self) -> bool:
        """Returns True if this set is empty, False otherwise."""
        return not bool(self.intervals)

    @property
    def is_singleton(self) -> bool:
        """Returns True if this set is a singleton, False otherwise."""
        return len(self.intervals) == 1 and self.intervals[0].lower == self.intervals[0].upper

    @property
    def value(self) -> float:
        """Returns the value of the set if it is a singleton. Raises an exception if the set is not a singleton."""
        if not self.is_singleton:
            raise ValueError("Cannot get value of a non-singleton set.")
        return self.intervals[0].lower  # or self.intervals[0].upper, they are equal for singletons

    # Other special methods
    def __hash__(self) -> int:
        """Returns the hash of the data in this set."""
        return hash(tuple(self.intervals))

    def __repr__(self) -> str:
        """Returns a string representation of this set. If the set is an interval a more compact representation is
        used."""
        if self.is_empty:
            return "FloatSet()"

        if self.is_interval:
            interval = self.intervals[0]
            if interval.left == portion.CLOSED and interval.right == portion.CLOSED:
                return f"FloatSet.closed({interval.lower}, {interval.upper})"
            elif interval.left == portion.OPEN and interval.right == portion.CLOSED:
                return f"FloatSet.openclosed({interval.lower}, {interval.upper})"
            elif interval.left == portion.CLOSED and interval.right == portion.OPEN:
                return f"FloatSet.closedopen({interval.lower}, {interval.upper})"
            elif interval.left == portion.OPEN and interval.right == portion.OPEN:
                return f"FloatSet.open({interval.lower}, {interval.upper})"

        return super().__repr__()
