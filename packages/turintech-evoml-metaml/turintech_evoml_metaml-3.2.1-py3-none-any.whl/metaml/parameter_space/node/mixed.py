import random


from typing import Union, Literal, Any
from metaml.parameter_space.set import (
    MixedSet,
    IntegerSet,
    FloatSet,
    CategoricalSet,
    FloatDistribution,
    IntegerDistribution,
)
from .base import ParameterNode, UNSET, UNSET_T


PureSetType = Union[FloatSet, IntegerSet, CategoricalSet]


class MixedNode(ParameterNode[MixedSet]):
    """A node in the parameter space that represents a mixed value.

    Attributes
    ----------
        domain (MixedSet): The domain of the parameter, represented as a set.

    """

    domain: MixedSet
    default_value: Union[Any, UNSET_T] = UNSET
    float_distribution: FloatDistribution = FloatDistribution.UNIFORM
    integer_distribution: IntegerDistribution = IntegerDistribution.UNIFORM
    primary_type: PureSetType = FloatSet

    def choose_subset(self, domain: MixedSet) -> PureSetType:
        """Get a random non-empty subset from the domain."""
        if non_empty_sets := [
            s_set for s_set in [domain.float_set, domain.integer_set, domain.categorical_set] if not s_set.is_empty
        ]:
            # Select a random set from the non-empty sets
            return random.choice(non_empty_sets)
        raise ValueError("All subsets of the domain are empty.")

    def sample(self, domain: Union[MixedSet, FloatSet, IntegerSet, CategoricalSet]) -> MixedSet:
        """Take a sample from a given domain."""
        if domain.is_empty:
            raise ValueError("Cannot sample from an empty set.")

        subset = self.choose_subset(domain) if isinstance(domain, MixedSet) else domain
        if isinstance(subset, IntegerSet):
            sampled_value = subset.sample(distribution=self.integer_distribution)
            return MixedSet(integer_set=sampled_value)
        elif isinstance(subset, FloatSet):
            sampled_value = subset.sample(distribution=self.float_distribution)
            return MixedSet(float_set=sampled_value)
        elif isinstance(subset, CategoricalSet):
            sampled_value = subset.sample()
            return MixedSet(categorical_set=sampled_value)

        raise NotImplementedError(f"Sampling from unsupported type {type(subset)} in mixed domain.")

    @property
    def maximum_categorical_domain(self) -> CategoricalSet:
        """Return the domain if the parameter is enabled, otherwise return a singleton of the default value."""
        if self.enabled:
            return self.domain.categorical_set
        return MixedSet.unit(self.default_value).categorical_set
