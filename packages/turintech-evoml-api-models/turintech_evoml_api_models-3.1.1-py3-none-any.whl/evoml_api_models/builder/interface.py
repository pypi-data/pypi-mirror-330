"""This module defines the abstract interface for the builder pattern applied to
Pydantic models. See the following link for more information:
    https://github.com/samuelcolvin/pydantic/issues/2152

As a summary, this pattern provides a convenient way to create large pydantic
models with many required fields, by adding them 1 at a time and validating when
ready.
"""
from pathlib import Path
from typing import Any, Generic, Mapping, Optional, Type, TypeVar, Union
from abc import ABC, abstractmethod

from pydantic.v1 import BaseModel, Protocol


ModelT = TypeVar("ModelT", bound=BaseModel)


class AbstractBuilder(Generic[ModelT]):
    """Defines the interface for a class building pydantic models, allowing to
    set fields one by one and return a pydantic model instance when all required
    fields have been set
    """

    _model_t: Type[ModelT]

    def __init__(self, model_t: Type[ModelT]):
        """The model class to be built has to be given when instanciating the
        builder
        """
        self._model_t = model_t


    # ----------------------------- construction ----------------------------- #
    @abstractmethod
    def parse_obj(self, obj: Mapping):
        """Loads fields into the builder from a map-like object (dictionaries,
        pydantic models, ...)

        Similar to pydantic model's `parse_obj`, without performing validation
        (validation happens on `self.build()`)
        """


    @abstractmethod
    def parse_file(
        self,
        path: Union[str, Path],
        *,
        content_type: Optional[str] = None,
        encoding: str = "utf-8",
        proto: Optional[Protocol] = None,
        allow_pickle: bool = False,
    ):
        """Takes in a file path, reads the file and passes the contents to
        parse_raw. If content_type is omitted, it is inferred from the file's
        extension.
        Adds the fields in the content to the current builder, overwriting
        existing fields.

        Similar to pydantic model's `parse_file`, without performing validation
        (validation happens on `self.build()`)
        """


    @abstractmethod
    def parse_raw(
        self,
        b: Union[str, bytes],
        *,
        content_type: Optional[str] = None,
        encoding: str = 'utf8',
        proto: Optional[Protocol] = None,
        allow_pickle: bool = False,
    ):
        """This takes a str or bytes and parses it as json, then passes the
        result to parse_obj. Parsing pickle data is also supported by setting
        the content_type argument appropriately.
        Adds the fields in the content to the current builder, overwriting
        existing fields.

        Similar to pydantic model's `parse_raw`, without performing validation
        (validation happens on `self.build()`)
        """


    # ------------------------------ validation ------------------------------ #
    @abstractmethod
    def build(self) -> ModelT:
        """Returns a valid instance of the pydantic model being built"""
