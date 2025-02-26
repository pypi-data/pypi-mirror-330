from typing import Optional


class MetaMLException(Exception):
    """Global MetaML error"""

    message: str = "MetaML internal error."

    def __init__(self, msg: Optional[str] = None):
        super().__init__(msg or self.message)


class ParseKwargsException(MetaMLException):
    """Raised when MLFactory encounters an error while parsing keyword arguments."""

    message = "An error has occurred while parsing compound keyword arguments."


class PredictProbaException(MetaMLException):
    """Raised when there is an error while predicting label probabilities"""

    message = "An error has occurred while predicting label probabilities."


class ForecastIndexException(MetaMLException):
    """Raised when the time index is incorrectly set or handled."""

    message = "An error has occurred relating to the time index."


class TargetTransformerException(MetaMLException):
    """Raised when an error occurs while apply a target transformation."""

    message = "An has occured while applying a target transformation."


class ConstraintException(MetaMLException):
    """Raised when an error occurs while handling constraints."""

    message = "An error has occurred while handling constraints."


class HugsLoadException(MetaMLException):
    """Raised when an error occurs while loading a HuggingFace model."""

    message = "An error has occurred while loading a HuggingFace model."


class IOException(MetaMLException):
    """Raised when an error occurs while saving or loading a model."""

    message = "An error has occurred while saving or loading a model."


class IndexTypeException(MetaMLException):
    """Raised when an index is of the wrong type."""

    message = "A type error has occurred while handling the index."


class MissingDataException(MetaMLException):
    """Raised when there is missing data."""

    message = "Missing data has been detected."


class OptunaCategoricalConstraintViolation(MetaMLException):
    """Raised when an error occurs while suggesting a categorical parameter to an Optuna trial."""

    message = "The sampled categorical value is not in the allowed domain."
