#!/usr/bin/env python3
# encoding: utf-8
"""
This file validates the input parameters for each model and give the validation status (true or false) and messages.
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
import itertools
import numpy as np
from typing import Dict, Optional, Any, List, Set, Tuple, Union, Type
from math import log10, ceil
from enum import Enum
from pydantic import StrictInt, BaseModel, ValidationError, parse_obj_as
from pydantic.error_wrappers import ErrorWrapper


from metaml.meta_models.names import ModelNameType
from metaml.factory import factory


logger = logging.getLogger("metaml")


# Parameter models definition
class StageNames(str, Enum):
    FILTERING = "filtering"
    TUNING = "tuning"
    STACKING = "stacking"
    RANDOM_SEARCH = "random-search"


class Stage(BaseModel):
    name: StageNames
    index: int


class InputParameter(BaseModel):
    parameterName: str
    parameterType: str
    fixedValue: Optional[bool] = False
    minValue: Optional[Union[StrictInt, float]] = None
    maxValue: Optional[Union[StrictInt, float]] = None
    values: List[Any]
    defaultValue: Any
    constraintInformation: Optional[str] = None


class ModelMetadata(BaseModel):
    model: ModelNameType


class ModelParameters(BaseModel):
    inputParameters: List[InputParameter]

    class Config:
        allow_mutation = True


class EvoMLModelDefinition(BaseModel):
    """Definition of the parameter space for a single model. This does not
    perform advanced validation.
    """

    name: ModelNameType
    parameters: Optional[ModelParameters] = None


# ---------------------------- validation message ---------------------------- #
# @TODO: move this somewhere else
KeyPosition = List[Union[int, str]]


class ValidationLevel(str, Enum):
    WARNING = "warning"
    ERROR = "error"


class ValidationConstraint:
    """Classes indicating a constraint on multiple keys of a given json
    (pydantic model). This class gives a message feedback to an user to provide
    feedback on modifications (warning) or rejection (error) of a given input
    model.

    Example
    -------
    {
        "hello": "world",
        "coordinates": [{"x": 0, "y": 7, "z": 4}, {"x": 2, "y": 5, "z": 1}],
    }

    We can indicate a problem with the constraint "x + y + z ≤ 10" with:

    ```
    message = ValidationConstraint(
        "The constraint: 'x + y + z ≤ 10' is not respected",
        ["coordinates", 0, "x"],
        ["coordinates", 0, "y"],
        ["coordinates", 0, "z"],
    )
    ```
    """

    __slots__ = ["positions", "message", "level", "number"]
    _count: int = 1  # Counting validation errors

    positions: List[KeyPosition]
    message: str
    level: ValidationLevel
    number: int

    def __init__(
        self,
        message: str,
        *key_positions: KeyPosition,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        self.positions = list(key_positions)
        self.message = message
        self.level = level
        self.number = self._count

        self.__class__._count += 1  # Increment the class level count

    def to_validation_error(self, model_class: Type[BaseModel]) -> ValidationError:
        """Converts this validation constraint message to a validation error"""
        assert self.level == ValidationLevel.ERROR

        ConstraintError = ValueError

        # Create the main exception (for the root level)
        errors = [
            ErrorWrapper(
                ConstraintError(f"Constraint Error {self.number}: {self.message}"),
                tuple(),
            ),
        ]

        # Create individual exceptions for each field involved in the constraint
        field_exc = ConstraintError(f"Constraint Error {self.number}")
        errors.extend(ErrorWrapper(field_exc, pos) for pos in self.positions)
        return ValidationError(
            errors=errors,
            model=model_class,
        )


def constraint_validation(
    model_definition: EvoMLModelDefinition,
) -> Tuple[EvoMLModelDefinition, List[ValidationConstraint]]:
    """Verifies if a given model definition satisfies the constraints associated
    with its parameters.

    Arguments:
        model_definition (EvoMLModelDefinition):
            Instance of ModelDefinition that is valid for parsing (types & keys
            are correct) but might not satisfy the parameters constraints.

    Returns:
        EvoMLModelDefinition:
            Updated instance of ModelDefinition injecting default parameters and
            restricting values for constrained parameters.

        List[ValidationMessages]:
            List of messages giving feedback on the json. Messages with an error
            level indicate that this is rejected (invalid for the constraints),
            whereas warning level indicates that changes were made to ensure
            validity.
    """
    # @TODO: make sure this properly edits the instance returned. We're
    # modifying elements placed in a map (vs. original list) expecting them to
    # be mutable, but this should be tested.
    messages: List[ValidationConstraint] = []

    # ------------------------- initialise variables ------------------------- #
    # Input Parameters are provided as a list. We convert them to maps of
    # {name → parameter} for convenience

    # Parameters given as input. We need to validate them against the reference
    # parameters and the reference constraints.
    # → single parameters: [A, B, C, D]
    parameters: Dict[str, InputParameter] = {
        input.parameterName: input for input in model_definition.parameters.inputParameters
    }

    # Reference parameters. Official information about supported parameters and
    # their spaces.
    # → single parameters: [A, B, C, D]
    ref_parameters: Dict[str, InputParameter] = {
        input.parameterName: input
        for input in parse_obj_as(
            List[InputParameter],
            factory.get_simple_param_by_name(model_definition.name).dict()["inputParameters"],
        )
    }

    # get_param_by_name → [A~B, C, D]
    # Provides constraints and the single variables that are not part of any
    # constraints
    reference_definition = EvoMLModelDefinition(
        name=model_definition.name,
        parameters=ModelParameters.parse_obj(factory.get_param_by_name(model_definition.name).dict()),
    )

    # Reference constraints. Provides information on constraints between 2 or
    # more single parameters.
    # → contraints: [A~B]
    ref_constraints: Dict[str, InputParameter] = {
        input.parameterName: input
        for input in reference_definition.parameters.inputParameters
        if "~~~" in input.parameterName  # extract only the constraints
    }

    # ---------------------------- error handling ---------------------------- #
    # Small utilitied to prepare for giving error on specific parameter's fields
    def get_index(name: str) -> int:
        """Finds the index of an input parameter with a given name"""
        # Note: this is needed to give error feedbacks, as the map structure
        # makes us loose track of where each parameter is in the initial model
        for i, input_p in enumerate(model_definition.parameters.inputParameters):
            if name in input_p.parameterName:
                return i
        logger.error(f"Parameter with name {name} not found in list.")
        # temp fix if parameter is not found
        return -1

    parameters_position = ["parameters", "inputParameters"]

    # --------------------------- inject defaults ---------------------------- #
    # 1. Inject missing parameters in the input.
    for name, input_p in ref_parameters.items():
        if name not in parameters:
            parameters[name] = input_p
            # currently if a param is not in parameters, it
            # means that it is set to the default value
            parameters[name].fixedValue = True

    if not ref_constraints:
        return model_definition, []  # No need for validation feedback

    for constraint, constraint_values in ref_constraints.items():
        # A constraint looks like:
        # 'A~~~B' which is single parameters [A, B] joined by '~~~'
        constrained_params = constraint.split("~~~")

        # ------------------- building the reference space ------------------- #
        # The reference space R should be a finite list of every accepted value
        # for the combination of values for the N members of the constraint
        # (e.g. [A~B] → N = 2).
        # It will be a list of any number of N-tuples (string types).
        #
        # Example:
        #   R for A~B → [('0', 'true'), ('0', 'false'), ('1', 'true')]
        #
        # Note:
        #   This is stored as ['0~~~true', '0~~~false', '1~~~true'] in the model
        reference_space: Set[Tuple[str, ...]] = {
            tuple(string_value.split("~~~")) for string_value in constraint_values.values
        }

        # --------------------- building the input space --------------------- #
        # We start by building the individual spaces for A and B.
        separate_spaces: Dict[str, List[str]] = {}
        for param_name in constrained_params:
            param = parameters[param_name]

            if param.fixedValue:
                # If the value is fixed, the space is a singleton. This is valid
                # for all types.
                separate_spaces[param_name] = [str(param.defaultValue)]
            else:
                # Handle each parameterType separately
                separate_spaces[param_name] = []
                if param.parameterType == "list":
                    separate_spaces[param_name] = list(map(str, param.values))
                    if param.defaultValue not in separate_spaces[param_name]:
                        separate_spaces[param_name].append(str(param.defaultValue))
                    if param.minValue is not None and param.maxValue is not None:
                        if isinstance(ref_parameters[param_name].minValue, int):
                            separate_spaces[param_name] += list(map(str, range(param.minValue, param.maxValue + 1)))
                        else:
                            gap = (param.maxValue - param.minValue) / 1000.0
                            exponential = ceil(log10(gap))
                            valid_float_numbers = list(np.arange(param.minValue, param.maxValue, 10**exponential)) + [
                                param.maxValue
                            ]
                            separate_spaces[param_name] += list(map(str, valid_float_numbers))

                elif param.parameterType == "int":
                    separate_spaces[param_name] = list(map(str, range(param.minValue, param.maxValue + 1)))

                elif param.parameterType == "boolean":
                    separate_spaces[param_name] = ["True", "False"]

                elif param.parameterType == "float":
                    gap = (param.maxValue - param.minValue) / 1000.0
                    exponential = ceil(log10(gap))
                    valid_float_numbers = list(np.arange(param.minValue, param.maxValue, 10**exponential)) + [
                        param.maxValue
                    ]
                    separate_spaces[param_name] = list(map(str, valid_float_numbers))

                else:
                    # @TODO: this should be solved by using an enum instead of
                    # a string for the type of this field
                    messages.append(
                        ValidationConstraint(
                            f"Invalid parameterType {param.parameterType}",
                            parameters_position + [get_index(param_name), "parameterType"],
                        )
                    )

        # The input space I is a finite list of every combination of the
        # constrained parameters A & B as provided by the user.
        # It will be a list of any number of N-tuples (string types).
        #
        # We build this with the cartesian product of the individual spaces in
        # the order in which they're listed in the constraint:
        #
        # I = space(A) x space(B)
        input_space: List[Tuple[str, ...]] = list(
            itertools.product(*[separate_spaces[name] for name in constrained_params])
        )
        # set intersection is not used as we want to keep the order of the input_space
        intersection = [x for x in input_space if x in reference_space]
        if intersection == input_space:
            # Entirely correct input space, not change needed
            # Note: this means that A & B will be expressed as independant
            # spaces of which the product is entirely valid.
            ...
        elif intersection:
            # Non empty intersection (and ≠ I) means that we have some invalid
            # points in I and we need to update the model + provide a warning

            # Remove the individual parameters from the model (e.g. [A, B])
            model_definition.parameters.inputParameters = [
                parameter
                for parameter in model_definition.parameters.inputParameters
                if parameter.parameterName not in constrained_params
            ]

            # Insert a constrained parameter expressing the combined space [A~B]
            combined_parameter = ref_constraints[constraint].copy()
            combined_parameter.values = ["~~~".join(element) for element in intersection]
            combined_parameter.defaultValue = combined_parameter.values[0]
            model_definition.parameters.inputParameters.append(combined_parameter)

            message = "Removed {n} invalid elements from the search space of the parameters {space}.\n\n".format(
                n=len(input_space) - len(intersection),
                space=" x ".join(constrained_params),
            )
            message += constraint_values.constraintInformation

            messages.append(
                ValidationConstraint(
                    message,
                    *[parameters_position + [get_index(p_name), "values"] for p_name in constrained_params],
                    level=ValidationLevel.WARNING,
                )
            )
        else:
            # Intersection of I & R is empty means that there's no valid points,
            # we reject the model

            message = "The search space for the parameters {space} doesn't contain any valid elements.\n\n".format(
                space=" x ".join(constrained_params),
            )
            message += constraint_values.constraintInformation

            messages.append(
                ValidationConstraint(
                    message,
                    *[parameters_position + [get_index(p_name), "values"] for p_name in constrained_params],
                )
            )
            ...

    return model_definition, messages
