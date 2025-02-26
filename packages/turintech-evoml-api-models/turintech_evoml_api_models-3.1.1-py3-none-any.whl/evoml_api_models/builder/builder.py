"""The module defines an implementation of the builder pattern defined in
.interface. Many details of the builder's behaviour are tied to LSP & completion
supported by python's type hint system.

This implementation "lies" to the typing system by pretenting the builder
instance created is an instance of the model it builds. It allows editors to
provide completion and typing on all the attributes you'll want to set when
building your model.

It also means that some methods (`dict`, `json`) might appear as existing when
they are not, and the methods unique to the builder (`build`) will appear as not
existing when they do.

See https://github.com/turintech/evoml-models/issues/8

Example:

    builder = get_builder(SomeModel)  # builder: 'SomeModel'
    builder.x = ...  # builder.x: 'int'
    builder.y = ...  # builder.x: 'int'
    builder.z = ...  # builder.x: 'int'
    some_model = builder.build()  # some_model: 'Any'

In the above example, the `builder.build()` method is not recognised, and as
such the returned instance, `some_model`, is not typed. We need to manually type
it:

    some_model: SomeModel = builder.build()  # some_model: 'SomeModel'

The interface provides functions to load fields from external objects. For
consistency, the interface is using the three equivalent methods in pydantic
models:

    - builder.parse_obj(...)
    - builder.parse_file(...)
    - builder.parse_raw(...)  # Not Implemented

This is just a shortcut to load many fields from an existing Map-like object
or file
"""
from __future__ import annotations
from typing import Union, Mapping, Optional, TypeVar, Type, Any
from inspect import isclass

from pydantic.v1 import BaseModel, Protocol

from pathlib import Path

from .interface import AbstractBuilder


ModelT = TypeVar("ModelT", bound=BaseModel)
T = TypeVar("T")


class ExtraModel(BaseModel):
    """Private class used as a backend to load json from raw bytes and files"""

    class Config:
        extra = "allow"

class Builder(AbstractBuilder[ModelT]):
    """Implementation of the AbstractBuilder interface. Provides the setter and
    getter methods to add attributes to the model, and the build method to
    provide an instance of the model builg built
    """

    _values: dict
    _build_cache: Optional[ModelT]

    def __init__(self, model_t: Type[ModelT]):
        super().__init__(model_t)
        self._build_cache = None
        self._values = {}

        for (name, field) in model_t.__fields__.items():
            # Note: field.outer_type can be List[X] and field.type_ will be X
            is_container = (field.outer_type_ != field.type_)
            is_model = isclass(field.type_) and issubclass(field.type_, BaseModel)

            if not is_container and is_model:
                # When we have a direct model instance (x: X), we create
                # a Builder[X] there
                setattr(self, name, Builder[field.type_](field.type_))
            elif not field.required:  # Set defaults for non-required fields
                setattr(self, name, field.get_default())


    def __setattr__(self, name: str, value: Any):
        """Sets the attributes in a cache dictionary for the model being built"""
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif isinstance(self._values.get(name), Builder) and isinstance(
            value, (dict, BaseModel)
        ):
            self._values[name].parse_obj(value)
        else:
            self._values[name] = value


    def __getattr__(self, name: str) -> Any:
        """Gets the attributes of the model being built"""
        # Pickle deals with an instance that didn't go through __init__ when
        # trying to call __setstate__.
        # In this case, _values doesn't exist, leading to an infinite loop.
        # We short-circuit this by raising an attribute error earlier.
        if name == "__setstate__":
            raise AttributeError()
        if name in self._values:
            return self._values[name]
        raise AttributeError()


    def __repr__(self) -> str:
        """Pydantic-like representation for builders"""
        fields = ", ".join([f"{k}={v}" for (k, v) in self._values.items()])
        model_name = self._model_t.__name__
        return f"{model_name}Builder({fields})"


    # ----------------------------- construction ----------------------------- #
    def _add_fields(self, mapping: dict):
        """Private method adding a set of fields (name → value dict) to this
        instance
        """
        assert isinstance(mapping, dict)
        for field, value in mapping.items():
            # Corner case: when we're absorbing values for a builder, we don't
            # want to "overwrite" the builder instance before build time. So we
            # need to handle builders differently
            if isinstance(getattr(self, field, None), Builder) and isinstance(value, dict):
                getattr(self, field)._add_fields(value)
            else:
                setattr(self, field, value)


    def parse_obj(self, obj: Mapping):
        model = ExtraModel.parse_obj(obj)
        self._add_fields(model.dict())


    def parse_raw(
        self,
        bytes_like: Union[str, bytes],
        *,
        content_type: Optional[str] = None,
        encoding: str = "utf-8",
        proto: Optional[Protocol] = None,
        allow_pickle: bool = False,
    ):
        model = ExtraModel.parse_raw(
            bytes_like,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle,
        )
        self._add_fields(model.dict())


    def parse_file(
        self,
        path: Union[str, Path],
        *,
        content_type: Optional[str] = None,
        encoding: str = "utf-8",
        proto: Optional[Protocol] = None,
        allow_pickle: bool = False,
    ):
        model = ExtraModel.parse_file(
            path,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle,
        )
        self._add_fields(model.dict())


    # ------------------------------ validation ------------------------------ #
    def _to_dict(self) -> dict:
        """Converts a builder to a dictionary of {field → value},
        recursively (converts any Builder value to dict as well)
        """
        # We're not exposing this method because one of the particularities
        # of builders is that you should seldom access their values or
        # convert them to dictionary if they've not been "built" (validated)
        # into a safe model
        cleaned_values = {}

        convert = lambda x: x._to_dict() if isinstance(x, Builder) else x

        for (field, value) in self._values.items():
            if isinstance(value, list):
                cleaned_values[field] = list(map(convert, value))
            elif isinstance(value, tuple):
                print(value, type(value))
                cleaned_values[field] = tuple(map(convert, value))
            else:
                cleaned_values[field] = convert(value)
        return cleaned_values


    def build(self, cache: bool = True) -> ModelT:
        """Returns a (validated) instance of the model being build.

        Recursively builds fields that are models themselves.
        """
        # Implementation details: if we build recursively using the build
        # method, we'll end up with a very obscure validation error when
        # something fails (i.e. no context of which level caused the crash)

        if not cache:
            return self._model_t.parse_obj(self._to_dict())

        # Parse the local dictionary of values
        if self._build_cache is None:
            self._build_cache = self.build(cache=False)
        return self._build_cache


def get_builder(model_t: Type[ModelT]) -> Builder[ModelT]:
    """Provides a builder for the given pydantic model class.

    IMPORTANT: always postfix the output of this function with the word
    'builder' to keep in mind that it's a builder.

    This implementation "lies" to the typing system by pretenting the builder
    instance created is an instance of the model it builds. It allows editors to
    provide completion and typing on all the attributes you'll want to set when
    building your model.

    It also means that some methods (`dict`, `json`) might appear as existing when
    they are not, and the methods unique to the builder (`build`) will appear as not
    existing when they do.

    See https://github.com/turintech/evoml-models/issues/8

    Example:

        builder = get_builder(SomeModel)  # builder: 'SomeModel'
        builder.x = ...  # builder.x: 'int'
        builder.y = ...  # builder.x: 'int'
        builder.z = ...  # builder.x: 'int'
        some_model = builder.build()  # some_model: 'Any'

    In the above example, the `builder.build()` method is not recognised, and as
    such the returned instance, `some_model`, is not typed. We need to manually type
    it.

    Example:
        builder = get_builder(SomeModel)  # builder: 'SomeModel'
        builder.x = ...  # builder.x: 'int'
        builder.y = ...  # builder.x: 'int'
        builder.z = ...  # builder.x: 'int'
        some_model: SomeModel = builder.build()  # some_model: 'SomeModel'
    """
    return Builder[ModelT](model_t)


__all__ = ["Builder", "get_builder"]
