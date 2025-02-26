"""Defines an abstract factory that can be used to easily create factories"""
# @TODO: this file is very generic and should be moved to a library
# (evoml_utils)?
from __future__ import annotations
from typing import Type, TypeVar, Generic, Dict, Optional, List
from enum import Enum
import logging


InterfaceT = TypeVar("InterfaceT")
EnumT = TypeVar("EnumT", bound=Enum)


class AbstractFactory(Generic[EnumT, InterfaceT]):
    """Abstract class implementing the generic behaviour of a factory,
    i.e. mapping an enum/name to an implementation of a common interface
    """

    # The registry exists on the level of the AbstractClassFactory, and will be
    # shared by all Factories subclassing it.
    # We need to have as first key of the registry the current factory class
    # (implementing the AbstractFactory) to keep those registries separate.
    registry: Dict[Type[AbstractFactory], Dict[EnumT, Type[InterfaceT]]] = {}

    logger = logging.getLogger("factory")

    @classmethod
    def register(cls, name: EnumT, impl: Type[InterfaceT]) -> Type[InterfaceT]:
        """Class method to register new abstract implementations to the internal registry.
        Args:
            name (str):
                The name of the entity to register.
            impl (Type[InterfaceT]):
                A class implementing the given interface
        Returns:
            The class (impl) that was registered
        """
        cls.set_item(name, impl)
        return impl


    @classmethod
    def create(cls, name: EnumT, *args, **kwargs) -> Optional[InterfaceT]:
        """Factory command to create an instance of an abstract implementation
        based on its name.
        Passes all arguments (*args, **kwargs) after the name to the class being
        instanciated.
        Args:
            name (EnumT):
                The name of the implementation to instanciate.
            args (*):
                Any number of positional arguments to provide to the chosen
                implementation.
            kwargs (**):
                Any number of keyword arguments to provide to the chosen
                implementation.
        Returns:
            An instance of the abstract interface.
        """
        ImplementationClass = cls.get_item(name)  # pylint: disable=C0103
        if ImplementationClass is None:
            return None
        instance = ImplementationClass(*args, **kwargs)
        return instance


    @classmethod
    def get_item(cls, key: EnumT) -> Optional[Type[InterfaceT]]:
        """Gets the class implementation of the current interface for a given
        name/enum. Returns None if the requested implementation does not exist.
        """
        # This is required, because Python shares the dictionary of a parent
        # class with class inheriting it
        registry = cls.registry.setdefault(cls, {})

        implementation = registry.get(key)
        if implementation is None:
            cls.logger.warning("Implementation %s does not exist in the registry", key)
        return implementation


    @classmethod
    def set_item(cls, key: EnumT, implementation: Type[InterfaceT]):
        """Sets an item in a specific key of the subclass' item store
        """
        # This is required, because Python shares the dictionary of a parent class
        # with class inheriting it
        registry = cls.registry.setdefault(cls, {})
        registry[key] = implementation


    @classmethod
    def get_registered(cls) -> List[EnumT]:
        """Get the list of registered implementations names"""
        return list(cls.registry.get(cls, {}).keys())


def new_factory(
    enum_t: EnumT, interface_t: InterfaceT
) -> Type[AbstractFactory[EnumT, InterfaceT]]:
    """Generates a new factory for the given enum and interface pair"""

    class Factory(AbstractFactory[EnumT, InterfaceT]):
        # No need for any code here, the generic class does all of the work
        ...

    Factory.__doc__ = f"""\
    Factory mapping the values of the '{enum_t.__name__}' enum to classes
    implementing the '{interface_t.__name__}' abstract interface.
    """

    return Factory[enum_t, interface_t]


__all__ = ["AbstractFactory", "new_factory"]