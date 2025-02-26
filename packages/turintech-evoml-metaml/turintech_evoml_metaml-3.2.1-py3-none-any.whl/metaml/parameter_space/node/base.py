from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Union, Any, Literal
from pydantic import BaseModel, root_validator
from enum import Enum


from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet, MixedSet


DomainSetT = TypeVar("DomainSetT", CategoricalSet, FloatSet, IntegerSet, MixedSet)
DomainSet = Union[CategoricalSet, FloatSet, IntegerSet, MixedSet]


UNSET_T = Literal["UNSET-SPECIAL-CONSTANT"]
UNSET: UNSET_T = "UNSET-SPECIAL-CONSTANT"
"""Special constant to indicate that a default value has not been set. None cannot be used since this is a valid setting
for some parameters."""


class ParameterNode(Generic[DomainSetT], BaseModel, ABC):
    """Base class for all parameter nodes. A parameter node represents a parameter, its domain and contains metadata
    for the UI.

    Attributes:
        name (str): The name of the parameter.
        label (str, optional): Label for UI display.
        description (str, optional): Description for UI display.
        domain (DomainSetType): The domain of the parameter, represented as a set.
        enabled (bool): Flag indicating if the parameter is enabled for tuning by default. Defaults to False.
        default_value (Any, optional): The default value for the parameter.
        constraint (bool): Flag indicating if there is a constraint. Defaults to False.
        constraintInformation (str, optional): Information about the constraint.
    """

    # Identifier
    name: str

    # UI display
    label: Optional[str]
    description: Optional[str]

    # Domain
    domain: DomainSetT
    enabled: bool = True
    default_value: Union[Any, UNSET_T] = UNSET

    # To be removed in the future. These attributes are currently still necessary to reproduce the parameter jsons, but
    # when we use the new parameter space for sampling from the parameter space we will not need these attributes
    # anymore.
    constraint: bool = False
    constraintInformation: Optional[str]

    class Config:
        extra = "forbid"

    @root_validator
    def validate_default_value_set(cls, values):
        enabled = values.get("enabled")
        default_value = values.get("default_value")
        if enabled is False and default_value == UNSET:
            raise ValueError("If enabled is False, default_value must not be UNSET.")
        return values

    @root_validator
    def validate_default_value_in_domain(cls, values: dict) -> dict:
        # default_value and domain can both be None so they may not be present in values
        default_value: Union[Any, UNSET_T] = values.get("default_value")
        domain: DomainSetT = values.get("domain")

        # enabled should always be present in values
        enabled: bool = values["enabled"]

        if not enabled and default_value not in domain:
            raise ValueError("Default value is not contained in the domain of the parameter.")

        return values

    @abstractmethod
    def sample(self, domain: DomainSetT) -> Any:
        """Sample a value from the domain of this parameter node."""
        ...

    def export_source_code(self):
        """Export the source code to reproduce this parameter node. Useful for programmatically generating the source
        code from existing parameter settings jsons."""
        return f"{self.name} = {self.__repr__()}"

    def __repr__(self) -> str:
        """Get a string representation of this parameter node which can be used to generate the source code for the
        node."""

        default_repr = super().__repr__()

        for field_name, field in self.__class__.__fields__.items():
            field_value = getattr(self, field_name)
            if isinstance(field_value, Enum):
                default_repr = default_repr.replace(field_value.__repr__(), f"'{field_value.value}'")

        return default_repr
