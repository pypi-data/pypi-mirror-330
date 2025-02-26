from typing import Literal, Union
from pydantic import StrictStr, StrictBool


from metaml.parameter_space.set import CategoricalSet
from .base import ParameterNode, UNSET, UNSET_T


class CategoricalNode(ParameterNode[CategoricalSet]):
    """A node in the parameter space that represents a categorical value.

    Attributes
    ----------
        domain (CategoricalSet): The domain of the parameter, represented as a set.

    """

    domain: CategoricalSet
    default_value: Union[StrictStr, StrictBool, UNSET_T, None] = UNSET

    def sample(self, domain: CategoricalSet) -> CategoricalSet:
        """Take a sample from a given domain."""
        return domain.sample()

    @property
    def maximum_categorical_domain(self) -> CategoricalSet:
        """Return the domain if the parameter is enabled, otherwise return a singleton of the default value."""
        if self.enabled:
            return self.domain
        return CategoricalSet.unit(self.default_value)
