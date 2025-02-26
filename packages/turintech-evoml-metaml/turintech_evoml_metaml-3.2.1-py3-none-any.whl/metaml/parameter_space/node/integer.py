from typing import Union, Literal
from pydantic import StrictInt

from metaml.parameter_space.set.integer import IntegerSet, IntegerDistribution
from .base import ParameterNode, UNSET, UNSET_T


class IntegerNode(ParameterNode[IntegerSet]):
    """A node in the parameter space that represents an integer value.

    Attributes
    ----------
        domain (IntegerSet): The domain of the parameter, represented as a set.
        distribution (IntegerDistribution): The distribution to use when sampling from the domain.
    """

    domain: IntegerSet
    distribution: IntegerDistribution = IntegerDistribution.UNIFORM
    default_value: Union[StrictInt, UNSET_T] = UNSET

    def sample(self, domain: IntegerSet) -> IntegerSet:
        """Take a sample from a given domain."""
        return domain.sample(distribution=self.distribution)
