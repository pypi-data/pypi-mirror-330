"""This module provides common validators for pydantic, along with a class and
a decorator allowing constructor-level validation for pydantic model
(specifically for getters)
"""
# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import TypeVar, Callable
from functools import wraps
import logging

# Dependencies
from pydantic.v1 import BaseModel
# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("models.tests_io")
logger.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------- #
S = TypeVar('S')  # pylint: disable=C0103
T = TypeVar('T')  # pylint: disable=C0103


# ---------------------------------------------------------------------------- #
class InstanceValidationModel(BaseModel):
    """This model subclasses pydantic's BaseModel to offer validation at
    instantiation time (see instance_validator decorator)
    """

    def __init__(self, *args, **kwargs):
        """Calls the validators defined at instance time"""
        super().__init__(*args, **kwargs)
        for validator in self.__get_instance_validators():
            validator(self)

    @classmethod
    def __get_instance_validators(cls):
        namespaces = [pclass.__dict__ for pclass in [cls] + list(cls.__bases__)]
        for _, value in [x for nspace in namespaces for x in nspace.items()]:
            is_validator = getattr(value, INSTANCE_VALIDATOR_CONFIG_KEY, False)
            if is_validator:
                yield value


# ──────────────────────────────────────────────────────────────────────────── #
Validator = Callable[[T], None]
INSTANCE_VALIDATOR_CONFIG_KEY = "__instance_validator__"
def instance_validator(validator: Validator) -> Validator:
    """Decorator providing the ability to validate a pydantic model's instance
    after it's instantiated, by decorating a method that takes `self` as its
    only parameter, and does not return any error.
    It should raise an exception if the instance is invalid.
    """
    @wraps(validator)
    def signature_check(*args, **kwargs):
        if len(args) != 1 or len(kwargs) > 0:
            raise ValueError(
                f"validator {validator} should have a single argument: `self`"
            )
        self = args[0]
        if not isinstance(self, InstanceValidationModel):
            raise ValueError(
                "@instance_decorator should only be used on method of "
                "InstanceValidationModel's subclasses"
            )
        return validator(*args, **kwargs)

    # We mark the function as a validator
    setattr(signature_check, INSTANCE_VALIDATOR_CONFIG_KEY, True)
    return signature_check
