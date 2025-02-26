from __future__ import annotations
import sys
import numpy as np
from typing import Optional
from pydantic import BaseModel, validator, StrictInt
from typing import List, Tuple
from enum import Enum


from metaml.parameter_space.set.base import BaseSet


class IntegerDistribution(str, Enum):
    """Enumeration of all supported integer distributions."""

    UNIFORM = "uniform"
    LOG_UNIFORM = "log-uniform"


class IntegerInterval(BaseModel):
    """Class that represents an integer interval where stop is exclusive. Empty intervals occur when start >= stop.

    Attributes
    ----------
    start: int
        Start of the interval.
    stop: int
        End of the interval, exclusive.
    """

    start: StrictInt
    stop: StrictInt  # Exclusive

    def intersection(self, other: IntegerInterval) -> IntegerInterval:
        """Compute the intersection of two integer intervals."""
        start = max(self.start, other.start)
        stop = min(self.stop, other.stop)

        return IntegerInterval(start=start, stop=stop)

    def difference(self, other: IntegerInterval) -> List[IntegerInterval]:
        """Compute the difference between two integer intervals."""
        if self.start >= other.start and self.stop <= other.stop:
            # other interval fully covers self interval
            return []

        if self.start < other.start and self.stop > other.stop:
            # other interval is fully inside self interval
            return [
                IntegerInterval(start=self.start, stop=other.start),
                IntegerInterval(start=other.stop, stop=self.stop),
            ]

        if self.start < other.start < self.stop:
            # other interval starts inside self interval and ends after
            return [IntegerInterval(start=self.start, stop=other.start)]

        if self.start < other.stop < self.stop:
            # other interval ends inside self interval and starts before
            return [IntegerInterval(start=other.stop, stop=self.stop)]

        # other interval is completely outside self interval
        return [IntegerInterval(start=self.start, stop=self.stop)]

    def __hash__(self) -> int:
        return hash((self.start, self.stop))


class IntegerSet(BaseSet):
    """Class that represents a set of integer intervals.

    Attributes
    ----------
    ranges: List[IntegerInterval]
        List of integer intervals in the set.
    """

    ranges: List[IntegerInterval] = []

    # Constructors
    @validator("ranges")
    def merge_ranges(cls, range_list: List[IntegerInterval]) -> List[IntegerInterval]:
        """Merge overlapping intervals to simplify and provide a unique representation of the data defining this set."""
        range_pairs = sorted([(interval.start, interval.stop) for interval in range_list])

        merged: List[IntegerInterval] = []
        for start, end in range_pairs:
            if start >= end:  # Ignore empty intervals
                continue

            if not merged or merged[-1].stop < start:
                merged.append(IntegerInterval(start=start, stop=end))
            else:
                merged[-1].stop = max(merged[-1].stop, end)

        return merged

    @classmethod
    def unit(cls, number: int) -> IntegerSet:
        """Create a set containing a single integer."""
        return cls(ranges=[IntegerInterval(start=number, stop=number + 1)])

    @classmethod
    def closed(cls, start: int, stop: int) -> IntegerSet:
        """Create a set containing all integers between start and stop, inclusive on both sides."""
        return cls(ranges=[IntegerInterval(start=start, stop=stop + 1)])

    @classmethod
    def closedopen(cls, start: int, stop: int) -> IntegerSet:
        """Create a set containing all integers between start and stop, inclusive of start but not stop."""
        return cls(ranges=[IntegerInterval(start=start, stop=stop)])

    @classmethod
    def from_tuples(cls, tuple_list: Optional[List[Tuple[int, int]]] = None) -> IntegerSet:
        """Create a set from a list of tuples, where each tuple represents an integer interval."""
        if tuple_list is None:
            tuple_list = []
        interval_list = [IntegerInterval(start=start, stop=stop) for start, stop in tuple_list]
        return cls(ranges=interval_list)

    # Set operations
    def union(self, other: IntegerSet) -> IntegerSet:
        """Compute the union of two integer sets."""
        if not isinstance(other, IntegerSet):
            raise TypeError("Input must be an instance of IntegerSet")
        return IntegerSet(ranges=self.ranges + other.ranges)

    def intersection(self, other: IntegerSet) -> IntegerSet:
        """Compute the intersection of two integer sets."""
        if not isinstance(other, IntegerSet):
            raise TypeError("Input must be an instance of IntegerSet")

        result_intervals = []  # Initialize an empty list to store the resulting intervals

        for interval1 in self.ranges:
            for interval2 in other.ranges:
                intersection = interval1.intersection(interval2)

                result_intervals.append(intersection)

        return IntegerSet(ranges=result_intervals)

    def difference(self, other: IntegerSet) -> IntegerSet:
        """Compute the difference between two integer sets."""
        if not isinstance(other, IntegerSet):
            raise TypeError("Input must be an instance of IntegerSet")

        result_ranges = []  # Initialize an empty list to store the resulting ranges

        for r1 in self.ranges:
            current_ranges = [r1]

            for r2 in other.ranges:
                new_ranges = []  # Initialize an empty list to store new ranges

                for cr in current_ranges:
                    diff = cr.difference(r2)
                    new_ranges.extend(diff)

                current_ranges = new_ranges

            result_ranges.extend(current_ranges)

        return IntegerSet(ranges=result_ranges)

    def sample(self, distribution: IntegerDistribution) -> IntegerSet:
        """Take a sample from a given domain and return a singleton set containing the sample."""
        if self.is_empty:
            raise ValueError("Cannot sample from an empty set.")

        if not self.is_interval:
            raise NotImplementedError(f"Sampling from a disconnected set is not yet supported: {self}.")

        if distribution == IntegerDistribution.UNIFORM:
            sample_value = np.random.randint(self.lower_bound, self.upper_bound)
        elif distribution == IntegerDistribution.LOG_UNIFORM:
            sample_value = int(np.exp(np.random.uniform(np.log(self.lower_bound), np.log(self.upper_bound))))
        else:
            raise ValueError(f"Invalid distribution specified: {distribution}.")

        return IntegerSet.unit(sample_value)

    # Properties
    @property
    def lower_bound(self) -> int:
        """Return the lower bound of the set. If the set is empty returns the largest possible integer."""
        return self.ranges[0].start if self.ranges else sys.maxsize

    @property
    def upper_bound(self) -> int:
        """Return the exclusive upper bound of the set. If the set is empty returns the smallest possible integer."""
        return self.ranges[-1].stop if self.ranges else -sys.maxsize

    @property
    def is_interval(self) -> bool:
        """Return True if the set is a single interval, False otherwise."""
        return len(self.ranges) == 1

    @property
    def is_empty(self) -> bool:
        """Return True if the set is empty, False otherwise."""
        return len(self.ranges) == 0

    @property
    def is_singleton(self) -> bool:
        """Returns True if this IntegerSet contains exactly one element, False otherwise."""
        return len(self.ranges) == 1 and self.ranges[0].start + 1 == self.ranges[0].stop

    @property
    def value(self) -> int:
        """Returns the single element of this IntegerSet if it is a singleton, otherwise raises a ValueError."""
        if self.is_singleton:
            return self.ranges[0].start
        raise ValueError("Cannot get value of a non-singleton set.")

    # Other special methods
    def __hash__(self) -> int:
        """Return a hash of the set."""
        return hash(tuple(self.ranges))

    def __repr__(self) -> str:
        """Return a string representation of the set. If the set is empty or an interval then a compact representation is used."""
        if self.is_empty:
            return "IntegerSet()"
        if self.is_interval:
            return f"IntegerSet.closedopen({self.lower_bound}, {self.upper_bound})"
        return super().__repr__()
