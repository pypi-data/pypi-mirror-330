# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from __future__ import annotations
from typing import (
    TypeVar,
    Type,
    List,
    Dict,
    Optional,
    Sequence,
    Any,
)
from pathlib import Path
import logging

# Dependencies
from pydantic.v1 import BaseModel, validator, Field
from pydantic.v1.generics import GenericModel

# Module
from .validation import InstanceValidationModel, instance_validator
from .interface import Readable, Writable

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("models.tests_io")
logger.setLevel(logging.WARNING)

Model = Type[BaseModel]

# ---------------------------------------------------------------------------- #
FileT = TypeVar('FileT')
class File(InstanceValidationModel):
    """A generic file (txt, zip, ...) at the given path. The `exists` field is
    here to create a File in write mode - no validation will be done against the
    path or its content.
    """
    is_builder: bool = Field(
        False,
        desciption="Flag that indicates the builder mode (no validation)",
    )
    path: Path

    # --------------------------- builder pattern ---------------------------- #
    @classmethod
    def builder(cls: Type[FileT], path: Path, **kwargs) -> FileT:
        """Builder pattern: creates an instance of this File subclass that is
        not validated, allowing you to access the path for writing.

        Once you're done building and want to use an instance for reading, you
        can use the `build()` method.
        """
        if "is_builder" in kwargs:
            kwargs.pop("is_builder")
        return cls(path=path, is_builder=True, **kwargs)

    def build(self: FileT) -> FileT:
        """Builder pattern: given an instance created with `File.builder`,
        returns a new instance that performs validation on the file that has
        been built.
        """
        assert self.is_builder, "This method should only be used on a builder folder"
        content = dict(is_builder=False, **self.dict(exclude={"is_builder"}))
        return self.__class__.parse_obj(content)

    # ------------------------------ validation ------------------------------ #
    @validator('path')
    def path_exists(cls, path: Path, values: Dict) -> Path:
        """Checks that the path exists"""
        if values.get("is_builder"):
            return path
        if not path.exists():
            logger.warning(
                "If you want to declare a file for writing, you can set `is_builder=True`"
            )
            raise FileNotFoundError(f"{path} does not exist")
        return path


    # ------------------------------- methods -------------------------------- #
    def write_text(self, data, encoding=None, errors=None):
        """ Open the file in text mode, write to it, and close the file. """
        self.path.write_text(data=data, encoding=encoding, errors=errors)


# ---------------------------------------------------------------------------- #
class MultiExtensionsFile(File):
    """A file with multiple valid extensions at the given base path. On
    instanciation, sets the path to be the first valid (existing) path using the
    list of providing extensions.

    This class is very generic, so you might want to create subclasses that set
    extensions to a specific value:

        class YamlFile(MultiExtentionFile):
            extensions: Sequence[str] = ['.yaml', '.yml']

    To make this process easier, the `with_extension` class method is a factory
    of subclasses setting extensions to a specific value:

        YamlFile = MultiExtensionFile.with_extensions(['.yaml', '.yml'])
    """
    extensions: Sequence[str] = ['.csv', '.parquet']

    # -------------------------------- utils --------------------------------- #
    @staticmethod
    def _check_extension(ext: str, extensions: Sequence[str] = None):
        """ Checks that the extension include the leading dot """
        if ext[0] != '.':
            raise ValueError(f"extension {ext} should start with '.'")
        if extensions and ext not in extensions:
            raise ValueError(f"Unexpected extension: extension={ext}, expected={extensions}")

    # ------------------------------- factory -------------------------------- #
    @classmethod
    def with_extensions(  # pylint: disable=E0602,W0613
        cls, file_extensions: List[str]
    ) -> Type[MultiExtensionsFile]:
        """Factory method returning subclasses of `MultiExtensionFile` that sets
        the `extension` field to a set of value. This is usefull if you know you
        might need to instanciate many files with the same set of extensions.
        """
        class SpecificExtensionsFile(cls):  # pylint: disable=C0115
            extensions: Sequence[str] = file_extensions
        return SpecificExtensionsFile

    # ------------------------------ validators ------------------------------ #
    @validator("path")
    def path_exists(cls, path: Path):  # pylint: disable=W0221
        """Cancel superclass' path_exists validation as the path might have
        different extensions, find_valid_extension should raise a FileNotFound
        error instead
        """
        return path

    @validator('extensions', always=True)
    def extensions_with_dot(cls, extensions: List[str]) -> List[str]:
        """Checks that extensions include the leading dot"""
        for ext in extensions:
            cls._check_extension(ext)
        return extensions

    # Here we need to set always = True because this validator operates on the
    # value of `path`, and should do so even for the default value of extensions
    @validator("extensions", always=True)
    def find_valid_extension(cls, extensions: List[str], values: dict) -> List[str]:
        """Finds a valid extension among the list, and overwrites the path.
        This should be done in a function validating path, but inheritance
        defines path before extensions, so we don't have access to extensions in
        path validation
        """
        if values.get("is_builder"):
            return extensions

        path: Path = values["path"]
        for ext in extensions:
            if path.with_suffix(ext).exists():
                values["path"] = path.with_suffix(ext)
                return extensions

        no_suffix = path.parent / path.stem
        raise FileNotFoundError(
            f"Did not find any valid file for {no_suffix} "
            f"with extensions {extensions}"
        )

    # ------------------------------- methods -------------------------------- #
    def get_file(self, extension: str) -> Path:
        """Compose the final path for the file with the given extension"""
        self._check_extension(ext=extension, extensions=self.extensions)
        return self.path.with_suffix(extension)

    def write_text(  # pylint: disable=W0221
        self, data: Any, extension: str = ".csv", encoding=None, errors=None
    ):
        """Open the file in text mode, write to it, and close the file."""
        file = self.get_file(extension=extension)
        file.write_text(data=data, encoding=encoding, errors=errors)

    def valid_paths(self) -> List[Path]:
        """Returns a list of all valid paths for this file, in order of priority
        """
        return [self.path.with_suffix(ext) for ext in self.extensions]


# ---------------------------------------------------------------------------- #
T = TypeVar('T')
ModelT = TypeVar('ModelT')
class JsonFile(GenericModel, Writable[ModelT], Readable[ModelT], File):
    """A json file, providing both the path and the modelType (BaseModel
    subclass) to load it.

    The generic notation is here to provide type hints on methods returning
    instances of modelType. It has no impact whatsoever at runtime.

    This class is very generic, so you might want to create subclasses that set
    model to a specific value:

        class ConfigFile(JsonFile):
            model: Type[Model] = Config

    To make this process easier, the `with_model` class method is a factory
    of subclasses setting model to a specific value:

        ConfigFile = JsonFile.with_model(Config)
    """
    model: Type[Model]
    loaded: Optional[ModelT] = None  # Note: _* & __* are protected in pydantic

    # ------------------------------- factory -------------------------------- #
    @classmethod
    def with_model(cls, model_type: Type[T]) -> Type[JsonFile[T]]:  # pylint: disable=W0613,R0201
        """Factory method returning subclasses of `JsonFile` that sets the
        `model` field.
        This is usefull if you know you might need to instanciate many files
        validated with the same pydantic model.
        """
        class SpecificModelFile(cls):  # pylint: disable=C0115
            model: Type[Model] = model_type
        return SpecificModelFile

    # ------------------------------ validation ------------------------------ #
    @instance_validator
    def _load_model(self):
        """Loads the json using `self.model` to validate its structure and
        content. To avoid loading twice the same model, we cache that loading in
        an attribute
        """
        if not self.is_builder:
            self.loaded: ModelT = self.model.parse_file(self.path)
        return self.loaded

    # ----------------------------- read & write ----------------------------- #
    def read(self) -> ModelT:
        """Reads the json file, returning an instance of `self.model`.
        Note: this reading is cached, so `read()` always returns the same
        instance
        """
        if self.is_builder:
            raise ValueError("You should not call `read` on a builder instance")
        return self.loaded if self.loaded is not None else self._load_model()

    def write(self, model: ModelT):
        """Writes an instance of `self.model` to `self.path`"""
        if not isinstance(model, self.model):
            raise TypeError(
                f"Wrong model class: expected={self.model}, received={model.__class__}"
            )
        self.write_text(model.json(indent=2))
