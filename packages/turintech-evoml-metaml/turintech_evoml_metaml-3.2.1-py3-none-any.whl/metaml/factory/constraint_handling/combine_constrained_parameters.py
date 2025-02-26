import numpy as np
import itertools


from typing import List, Dict
from math import log10, ceil


from metaml.exceptions import ConstraintException
from metaml.factory.parameter_settings import (
    ParamSettings,
    ParameterType,
    InputParameter,
    ConstrainedGroup,
    CompatibleSpaces,
    ParameterSpace,
)


def sample_from_spaces(spaces: List[ParameterSpace]) -> Dict[str, List]:
    # sampled_values maps parameters names to a list of sampled values
    sampled_values: Dict[str, List] = {}

    for parameter_space in spaces:
        if parameter_space.parameterType == ParameterType.LIST:
            value_list = list(parameter_space.values)
            if parameter_space.minValue is not None:
                if type(parameter_space.minValue) == int:
                    value_list += list(range(parameter_space.minValue, parameter_space.maxValue + 1))

                elif type(parameter_space.minValue) == float:
                    gap = (parameter_space.maxValue - parameter_space.minValue) / 1000.0
                    exponential = ceil(log10(gap))
                    valid_float_numbers = list(
                        np.arange(
                            parameter_space.minValue,
                            parameter_space.maxValue,
                            10**exponential,
                        )
                    )
                    valid_float_numbers.append(parameter_space.maxValue)
                    value_list += valid_float_numbers

            sampled_values[parameter_space.parameterName] = value_list

        elif parameter_space.parameterType == ParameterType.INT:
            sampled_values[parameter_space.parameterName] = list(
                range(parameter_space.minValue, parameter_space.maxValue + 1)
            )

        elif parameter_space.parameterType == ParameterType.FLOAT:
            gap = (parameter_space.maxValue - parameter_space.minValue) / 1000.0
            exponential = ceil(log10(gap))
            valid_float_numbers = list(
                np.arange(
                    parameter_space.minValue,
                    parameter_space.maxValue,
                    10**exponential,
                )
            )
            valid_float_numbers.append(parameter_space.maxValue)
            sampled_values[parameter_space.parameterName] = valid_float_numbers

    return sampled_values


def validate_constrained_group(constrained_group: ConstrainedGroup) -> None:
    """Every ConstrainedGroup is made of a list of CompatibleSpaces, each of which is a list of parameter spaces that
    can be combined without violating any constraints. Each CompatibleSpaces object in a ConstrainedGroup should refer
    to the same group of parameters in the same order. This function checks that this is the case.
    """

    if len(constrained_group) == 0:
        raise ConstraintException("ConstrainedGroup cannot be empty.")

    CompatibleSpacesParameterNames = List[str]  # A list of parameter names in a CompatibleSpaces object.

    compatible_spaces_parameter_names_reference = [
        parameter_space.parameterName for parameter_space in constrained_group[0]
    ]

    for compatible_spaces in constrained_group:
        compatible_spaces_parameter_names: CompatibleSpacesParameterNames = [
            parameter_space.parameterName for parameter_space in compatible_spaces
        ]
        if compatible_spaces_parameter_names != compatible_spaces_parameter_names_reference:
            raise ConstraintException(
                "All CompatibleSpaces in a ConstrainedGroup should refer to the same group of parameters and those "
                "parameters should be in the same order."
            )


def combine_constrained_group(
    constrained_group: ConstrainedGroup, input_parameters: Dict[str, InputParameter]
) -> InputParameter:
    """Combine a constrained group of parameters into a single complex parameter.

    Args:
        constrained_group (ConstrainedGroup):
            A list of CompatibleSpaces, each of which is a list of parameter spaces satisfying the constraints.

        input_parameters (Dict[str, InputParameter]):
            A dictionary mapping the names of all input parameters to their settings. Used to construct the default
            value of the complex parameter.

    Returns:
        InputParameter:
            The complex parameter which expresses the constrained parameters as a single unconstrained parameter.

    """

    # Check that the constrained group refers to a common set of parameters.
    validate_constrained_group(constrained_group)

    constrained_parameter_names: List[str] = [parameter_space.parameterName for parameter_space in constrained_group[0]]
    complex_parameter_name = "~~~".join(constrained_parameter_names)

    complex_parameter_values: List[str] = []

    compatible_spaces: CompatibleSpaces
    for compatible_spaces in constrained_group:
        sampled_values: Dict[str, List] = sample_from_spaces(compatible_spaces)
        # The cartesian product of the sampled values of each parameter in the constrained group is used to construct
        # the list of values for the complex parameter.
        complex_parameter_values.extend(
            [
                "~~~".join(str(value) for value in values_tuple)
                for values_tuple in itertools.product(*sampled_values.values())
            ]
        )

    complex_parameter_default_value: str = "~~~".join(
        str(input_parameters[name].defaultValue) for name in constrained_parameter_names
    )

    if complex_parameter_default_value not in complex_parameter_values:
        complex_parameter_values.append(complex_parameter_default_value)

    constraint_information = "Constraints:\n"
    for name in constrained_parameter_names:
        constraint_information += f"{name}: {input_parameters[name].constraintInformation}\n"

    return InputParameter(
        parameterName=complex_parameter_name,
        parameterType=ParameterType.LIST,
        label=complex_parameter_name,
        description=complex_parameter_name,
        minValue=None,
        maxValue=None,
        values=complex_parameter_values,
        defaultValue=complex_parameter_default_value,
        enabled=False,
        constraint=False,
        constraintInformation=constraint_information,
    )


def combine_constrained_parameters(original_parameters: ParamSettings) -> ParamSettings:
    """
    This function looks for constrained parameters in the original parameter settings. Parameters which share a
    constraint relationship are combined into a new parameter whose name is a combination of the names of the original
    parameters joined by ~~~. This complex parameter is treated as a categorical (list), and it replaces the constrained
    parameters in the original parameter dict. It has no constraint relationships with any other parameters. A list of
    allowed values is generated according to the constraints between the original parameters.

    Args:
        original_parameters (ParamSettings):
            The original parameters model. This contains an inputParameters field and optionally may contain
            constraintParameters describing the parameters which have a constraint relationship between them.

    Returns:
        ParamSettings: converted parameters with all constrained parameters replaced by unconstrained complex
        parameters.

    """

    input_parameters_dict: Dict[str, InputParameter] = {
        parameter.parameterName: parameter for parameter in original_parameters.inputParameters
    }

    # Parameters with no constraints can be added immediately to the new parameter settings.
    converted_params = ParamSettings(
        inputParameters=[
            input_parameter for input_parameter in original_parameters.inputParameters if not input_parameter.constraint
        ],
        metadata=original_parameters.metadata,
        parameters=original_parameters.parameters,
    )

    # We combine constrained parameters to form complex unconstrained parameters.
    if original_parameters.constraintParameters != None:
        constrained_group: ConstrainedGroup
        for constrained_group in original_parameters.constraintParameters:
            converted_params.inputParameters.append(combine_constrained_group(constrained_group, input_parameters_dict))

    return converted_params
