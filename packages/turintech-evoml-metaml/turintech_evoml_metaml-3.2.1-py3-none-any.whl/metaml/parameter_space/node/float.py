from pydantic import StrictFloat
from typing import Union


from metaml.parameter_space.set.float import FloatSet, FloatDistribution
from .base import ParameterNode, UNSET, UNSET_T


class FloatNode(ParameterNode[FloatSet]):
    """A node in the parameter space that represents a float value.

    Attributes
    ----------
        domain (FloatSet): The domain of the parameter, represented as a set.
        distribution (FloatDistribution): The distribution to use when sampling from the domain.
    """

    domain: FloatSet
    distribution: FloatDistribution = FloatDistribution.UNIFORM
    default_value: Union[StrictFloat, UNSET_T] = UNSET

    def sample(self, domain: FloatSet) -> FloatSet:
        """Take a sample from a given domain."""
        return domain.sample(distribution=self.distribution)
