from pydantic import (
    BaseModel,
    Extra,
    StrictInt,
    StrictBool,
    StrictStr,
    StrictFloat,
    root_validator,
)
from typing import List, Optional, Union, Set
from enum import Enum


from metaml.parameter_space.set import IntegerSet, FloatSet, CategoricalSet, MixedSet
from metaml.parameter_space.node import (
    IntegerNode,
    FloatNode,
    CategoricalNode,
    MixedNode,
)
from metaml.parameter_space.map import ConstraintEdge
from metaml.meta_models.metadata import MetaData


class ParameterType(str, Enum):
    INT = "int"
    FLOAT = "float"
    LIST = "list"
    BOOLEAN = "boolean"


class GenerateDistribution(str, Enum):
    STRING = "string"


class ParameterSpace(BaseModel):
    parameterName: str
    parameterType: ParameterType
    minValue: Optional[Union[StrictInt, StrictFloat]] = None
    maxValue: Optional[Union[StrictInt, StrictFloat]] = None
    values: Set[Union[StrictInt, StrictFloat, StrictStr, StrictBool]]

    class Config:
        extra = Extra.forbid


class InputParameter(ParameterSpace):
    defaultValue: Union[StrictInt, StrictFloat, StrictStr, StrictBool]
    label: str
    description: str
    enabled: bool
    constraint: bool
    constraintInformation: Optional[str] = None

    class Config:
        extra = Extra.forbid

    def to_parameter_node(
        self,
    ) -> Union[IntegerNode, FloatNode, CategoricalNode, MixedNode]:
        if self.parameterType == ParameterType.INT:
            return IntegerNode(
                name=self.parameterName,
                label=self.label,
                description=self.description,
                domain=IntegerSet.closed(self.minValue, self.maxValue),
                enabled=self.enabled,
                default_value=self.defaultValue,
                constraint=self.constraint,
                constraintInformation=self.constraintInformation,
            )
        elif self.parameterType == ParameterType.FLOAT:
            return FloatNode(
                name=self.parameterName,
                label=self.label,
                description=self.description,
                domain=FloatSet.closed(self.minValue, self.maxValue),
                enabled=self.enabled,
                default_value=self.defaultValue,
                constraint=self.constraint,
                constraintInformation=self.constraintInformation,
            )
        elif self.parameterType == ParameterType.BOOLEAN:
            return CategoricalNode(
                name=self.parameterName,
                label=self.label,
                description=self.description,
                domain=CategoricalSet({True, False}),
                enabled=self.enabled,
                default_value=self.defaultValue,
                constraint=self.constraint,
                constraintInformation=self.constraintInformation,
            )
        elif self.parameterType == ParameterType.LIST and self.minValue is None and self.maxValue is None:
            return CategoricalNode(
                name=self.parameterName,
                label=self.label,
                description=self.description,
                domain=CategoricalSet(self.values),
                enabled=self.enabled,
                default_value=self.defaultValue,
                constraint=self.constraint,
                constraintInformation=self.constraintInformation,
            )

        elif (
            self.parameterType == ParameterType.LIST
            and isinstance(self.minValue, int)
            and isinstance(self.maxValue, int)
        ):
            mixed_set = MixedSet(
                integer_set=IntegerSet.closed(self.minValue, self.maxValue),
                categorical_set=CategoricalSet(self.values),
            )
            return MixedNode(
                name=self.parameterName,
                label=self.label,
                description=self.description,
                domain=mixed_set,
                enabled=self.enabled,
                default_value=self.defaultValue,
                constraint=self.constraint,
                constraintInformation=self.constraintInformation,
            )
        elif (
            self.parameterType == ParameterType.LIST
            and isinstance(self.minValue, float)
            and isinstance(self.maxValue, float)
        ):
            mixed_set = MixedSet(
                float_set=FloatSet.closed(self.minValue, self.maxValue),
                categorical_set=CategoricalSet(self.values),
            )
            return MixedNode(
                name=self.parameterName,
                label=self.label,
                description=self.description,
                domain=mixed_set,
                enabled=self.enabled,
                default_value=self.defaultValue,
                constraint=self.constraint,
                constraintInformation=self.constraintInformation,
            )

        raise ValueError("Unsupported configuration.")


# CompatibleSpaces is a list of parameter spaces that can be combined in any way.
CompatibleSpaces = List[ParameterSpace]


# ConstrainedGroup specifies all allowed combinations of values of a group of parameters which share a constraint
# relationship. Each CompatibleSpaces object in a ConstrainedGroup should refer to the same group of parameters in the
# same order.
ConstrainedGroup = List[CompatibleSpaces]


class ParamSettings(BaseModel):
    parameters: List[Union[IntegerNode, FloatNode, CategoricalNode, MixedNode]]
    constraints: List[ConstraintEdge] = []
    metadata: MetaData

    inputParameters: List[InputParameter]  # Deprecated
    constraintParameters: Optional[List[ConstrainedGroup]] = None  # Deprecated.

    class Config:
        extra = Extra.forbid

    @root_validator(skip_on_failure=True)
    def check_prime_params_are_in_input_parameters(cls, values):
        """Check that the prime parameters are in the list of input parameters."""
        input_parameters = [parameter.parameterName for parameter in values["inputParameters"]]
        prime_parameters = values["metadata"].prime
        if missing_parameters := set(prime_parameters) - set(input_parameters):
            raise ValueError(f"Missing prime parameters: {missing_parameters}")

        return values

    def to_nodes(
        self,
    ) -> List[Union[CategoricalNode, FloatNode, IntegerNode, MixedNode]]:
        return [input_parameter.to_parameter_node() for input_parameter in self.inputParameters]
