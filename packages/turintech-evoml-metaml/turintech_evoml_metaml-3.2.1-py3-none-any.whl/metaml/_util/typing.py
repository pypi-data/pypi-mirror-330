from typing import Type, Iterable


def strict(collection_class: Type, element_class: Type):
    """Used to define the StrictCollection type for use in pydantic models."""

    class StrictCollection:
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v: Iterable):
            assert isinstance(v, collection_class)
            for x in v:
                assert isinstance(x, element_class)
            return v

    return StrictCollection
