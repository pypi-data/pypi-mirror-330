from typing import Dict, Any, Type
from enum import Enum
from pydantic import BaseSettings, Extra, BaseModel


NULL_STRING = "None"


class OverridableParametersModel(BaseSettings):
    """Base class for overridable parameters. These parameters can be controlled using an environment variable with the
    prefix metaml_"""

    class Config:
        env_prefix = "metaml_"
        extra = Extra.allow


class ParametersModel(BaseModel):
    """Base class for all parameter models. Overridable can be included in the OverridableParametersModel placed in
    the overridable field."""

    _overridable: Type[OverridableParametersModel] = OverridableParametersModel

    class Config:
        extra = Extra.forbid

    def __init__(self, **kwargs):
        """Overridable parameters are added to kwargs before being used to initialise the parameters model."""

        # Replace any "None" strings with None special constant
        for k, v in kwargs.items():
            if v == NULL_STRING:
                kwargs[k] = None

        overridable_params = dict(self._overridable(**kwargs))
        kwargs.update(**overridable_params)
        super().__init__(**kwargs)

    @property
    def external_representation(self) -> Dict[str, Any]:
        """Retrieve a dictionary of the parameters seen externally by evoml and the front end."""

        return {k: v.value if isinstance(v, Enum) else NULL_STRING if v is None else v for k, v in dict(self).items()}

    @property
    def internal_representation(self) -> Dict[str, Any]:
        """Retrieve a dictionary of the parameters used to initialise the internal model."""

        return {k: v.value if isinstance(v, Enum) else v for k, v in dict(self).items()}
