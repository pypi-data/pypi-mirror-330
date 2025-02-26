"""
In this module a base class is implemented with generic methods and properties
"""
# pylint: disable=W0246
#        W0246: Useless parent or super() delegation in method 'dict' (useless-parent-delegation)
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Dict, Any, List, Union, AbstractSet, Mapping, Optional, TypeVar

from pydantic.v1 import BaseModel
from pydantic.v1.fields import ModelField
from pydantic.v1.utils import to_camel

try:
    from pydantic.v1.main import ModelMetaclass as PydanticModelMetaclass
except:
    from pydantic.main import ModelMetaclass as PydanticModelMetaclass

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "BaseModelWithAlias",
    "BaseModelT",
    "BaseModelWithAliasT",
    "PropertyBaseModelT",
    "PropertyBaseModel",
    "AllOptional",
    "AllOptionalT",
]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Base Model Class                                                   #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class BaseModelWithAlias(BaseModel):
    """Base Model with enabled alias.
    Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias.
    """

    def dict(self, *args, by_alias: bool = True, **kwargs) -> Dict:
        """Generate a dictionary representation of the model, whose keys follow the JSON convention,
        optionally specifying which fields to include or exclude.
        """
        return super().dict(by_alias=by_alias, *args, **kwargs)

    def dict_py(self, *args, **kwargs):
        """Gets the dictionary whose keys follow the Python convention.
        It is the same behavior as the dict() method but with a more descriptive name.
            {
                "snake_case_key": value
            }
        """
        if kwargs and "by_alias" in kwargs:
            kwargs.pop("by_alias", None)
        return super().dict(by_alias=False, *args, **kwargs)

    def dict_json(self, *args, **kwargs):
        """Gets the dictionary whose keys follow the JSON convention by ensuring that 'aliases' are used as keys:
        {
            "camelCaseKey": value
        }
        """
        if kwargs and "by_alias" in kwargs:
            kwargs.pop("by_alias", None)
        return super().dict(by_alias=True, *args, **kwargs)

    def update(self, data: Dict[str, object]):
        # Data update
        for key, field in self.__fields__.items():
            if key in data or field.alias in data:
                setattr(self, key, data.get(key, data.get(field.alias)))
        # Data Validation
        self.__class__(**self.dict())

    @classmethod
    def get_field(cls, field_name: str, values: Dict) -> Any:
        """Retrieve the value of the field from the given dictionary searching by the field name and its alias.
        If exist a value for the field name and the alias, it will return the field name value
        """
        field: ModelField = cls.__fields__[field_name]
        return values.get(field.name, values.get(field.alias))

    class Config:
        """Class with base attributes for configuration"""

        @staticmethod
        def _is_camel_case(value: str):
            return value != value.lower() and value != value.upper() and "_" not in value

        @classmethod
        def _to_lower_camel(cls, value: str) -> str:
            """Returns the value in lower camel case.
            e.g. camelCase
            """
            # Here camel case refers to "upper camel case" aka pascal case
            # e.g. CamelCase.
            if cls._is_camel_case(value=value):
                return value
            camel_value = to_camel(value)
            return camel_value[0].lower() + camel_value[1:] if camel_value else camel_value

        # Use aliases in the JSON serialization in camel case instead of snake case
        alias_generator = _to_lower_camel

        # Recognizes both original name and alias as input
        allow_population_by_field_name = True


class PropertyBaseModel(BaseModel):
    """Base Model that overrides the dict function to include the object properties"""

    @classmethod
    def get_properties(cls):
        return [prop for prop, value in cls.__dict__.items() if isinstance(value, property)]

    @classmethod
    def is_prop_base(cls, base):
        if PropertyBaseModel in base.__bases__ or isinstance(base, PropertyBaseModel):
            return True
        return any((cls.is_prop_base(base=sub_base) for sub_base in base.__bases__))

    def dict_prop(self, **kwargs) -> Dict[str, Any]:
        return self.dict(show_prop=True, **kwargs)

    def dict(
        self,
        *,
        include: Optional[Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]]] = None,
        exclude: Optional[Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]]] = None,
        show_prop: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """Override the dict function to include our properties"""

        attributes = super().dict(include=include, exclude=exclude, **kwargs)

        if not show_prop:
            return attributes

        props = self.get_properties()
        self._add_bases_properties(
            base=self.__class__,
            attributes=attributes,
            props=props,
            dict_args=dict(include=include, exclude=exclude, **kwargs),
        )

        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attributes.update({prop: getattr(self, prop) for prop in props})

        return attributes

    def _add_bases_properties(self, base, attributes: Dict, props: List, dict_args: Dict):
        is_prop_base = False
        for sub_base in base.__bases__:
            if self.is_prop_base(base=sub_base):
                is_prop_base = True
                attributes.update(sub_base(**attributes).dict_prop(**dict_args))
            self._add_bases_properties(base=sub_base, attributes=attributes, props=props, dict_args=dict_args)
        if is_prop_base:
            props.extend(base.get_properties())

    class Config:
        """Class with base attributes for configuration"""

        validate_assignment = True


class AllOptional(PydanticModelMetaclass):
    """Makes Optional all the fields of a model"""

    def __new__(mcs, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            try:
                annotations.update(base.__annotations__)
            except AttributeError:
                pass
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(mcs, name, bases, namespaces, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Type definitions                                                   #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


BaseModelT = TypeVar("BaseModelT", bound=BaseModel)
BaseModelWithAliasT = TypeVar("BaseModelWithAliasT", bound=BaseModelWithAlias)
PropertyBaseModelT = TypeVar("PropertyBaseModelT", bound=PropertyBaseModel)
AllOptionalT = TypeVar("AllOptionalT", bound=AllOptional)
