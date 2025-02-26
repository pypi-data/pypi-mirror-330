# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from __future__ import annotations
from typing import (
    Callable,
    Union,
    Dict,
    List,
    Type,
    TypeVar,
)
from functools import wraps, partial
from pathlib import Path
from inspect import isclass
import logging

# Dependencies
from backports.cached_property import cached_property
from pydantic.v1 import validator

# Module
from .files import File

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("models.tests_io")
logger.setLevel(logging.WARNING)

# ---------------------------------- utils ----------------------------------- #
T = TypeVar('T')  # pylint: disable=C0103
def is_partial_subclass(
    subclass: Union[Type[T], partial], parent_class: Type[T]
) -> bool:
    """Checks if a given subclass is either a direct subclass or a partial
    subclass of the given parent class.
    """
    actual_subclass = subclass.func if isinstance(subclass, partial) else subclass
    return isclass(actual_subclass) and issubclass(actual_subclass, parent_class)


# ---------------------------------------------------------------------------- #
FileT = TypeVar('FileT', bound=File)
class Folder(File):
    """A folder existing in the given path. This class should be subclassed to
    provide attributes depending on that path (see @property decorator)
    """

    # --------------------------- builder pattern ---------------------------- #
    @classmethod
    def builder(cls: Type[FileT], path: Path, **kwargs) -> FileT:
        """Builder pattern: creates an instance of this Folder subclass that is
        not validated, allowing you to access the path of the different files
        for writing. Creates a folder at the given path if it doesn't exist.

        Every files of this folder are recursively in builder mode.

        Once you're done building and want to use an instance for reading, you
        can use the `build()` method.
        """
        path.mkdir(exist_ok=True)
        return super().builder(path=path, **kwargs)

    # ------------------------------ validation ------------------------------ #
    @validator('path')
    def path_is_folder(cls, path: Path, values: Dict) -> Path:
        """Check that the given path is a folder (on top of File's existing path
        check)
        """
        if values.get("is_builder"):
            return path
        if not path.is_dir():
            # The error if the file does not exist is covered in File
            raise FileNotFoundError(f"{path} is not a directory")
        return path

    # ------------------------------- methods -------------------------------- #
    def files(self) -> List[File]:
        """Returns the files defined by this specific folder instance"""
        files_instances = []
        for getter_name in self.files_names():
            files_instances += [getattr(self, getter_name)]
        return files_instances

    @classmethod
    def files_names(cls) -> List[str]:
        """Returns the name of all @files (file getters) defined by this class
        and its parent classes.
        """
        method_names = []
        # Retrieve the namespaces (including methods) for this class and its parents
        namespaces = [cls.__dict__] + [parent.__dict__ for parent in cls.__bases__]

        # Iterate over the methods looking for the FILES mark
        for name, method in [
            item for namespace in namespaces for item in namespace.items()
        ]:
            if getattr(method, FILES_CONFIG_KEY, False):
                method_names.append(name)

        return method_names

    class Config:  # pylint: disable=C0115
        # → pydantic does not support 'cached_property'
        # see https://github.com/samuelcolvin/pydantic/issues/1241
        keep_untouched = (cached_property,)


# ---------------------------------------------------------------------------- #
FILES_CONFIG_KEY = "__files_methods__"

FileT = TypeVar('FileT')
N = TypeVar('N')  # pylint: disable=C0103

# Note: the type annotation here is not accurate.
# ------------------------------------------------------
# The real type is:
# method:
#
#   `Callable[[Type[Folder]], Tuple[Path, Type[FileT]]]`
#
#   self → Path, FileT (class)
#
# decorated:
#
#   `Callable[Type[Folder], FileT]`
#
#   self → FileT (instance)
#
# ------------------------------------------------------
# However, to make the getters annotated properly, we prefer to lie on the
# initial method's annotation, and just keep that through the decoration
# process. This allows more control on the user side: whatetever the initial
# method defines will be kept as type annotation.
# ------------------------------------------------------
def files(method: Callable[..., FileT]) -> FileT:
    """Decorator that takes a getter for a given defined in a folder. The
    decorated method must take `self` (instance of `Folder`) as its unique
    argument, and must return a tuple of `Path` and a `File` class.
    Note that the `File` class returned should have a single requried argument:
    path. The function `partial` from functools can help creating such a class
    on the fly.

    It transforms that method to return an instance of the File class, using the
    given path. This decorator allows:
    - applying the property decorator to make the method a getter
    - disabling validation when using a folder in write mode
    - caching the file instanciation
    - easy gathering of the files defined by a folder accross inheritance

    Examples:

        @files
        def readme(self):
            return self.path / 'README.md', File

        @files
        def config(self):
            return self.path / 'config.json', JsonFile.with_model(Config)
    """
    # @property
    @wraps(method)
    @cached_property  # applies both @property (getter) & caching (singleton)
    def decorator(self: Type[Folder], *args, **kwargs):
        # 1. Signature validation
        if not isinstance(self, Folder):
            raise ValueError(
                "@files should only be used on method of Folder's subclasses"
            )

        # 2. Decorated method: instanciates the file depending on the mode
        returns = method(self)
        if not (isinstance(returns, tuple) and len(returns) == 2):
            raise TypeError(f"{method} should return a tuple of Path, Type[File]")

        file_class: Type[File]
        path, file_class = method(self, *args, **kwargs)
        if not isinstance(path, Path):
            raise TypeError(
                f"the first return of {method} should be a {Path}, found {path.__class__}"
            )

        if not is_partial_subclass(file_class, File):
            raise TypeError(
                f"the second return of {method} should be a {File}, found {file_class}"
            )

        # We instanciate as a builder if we're a builder ourselve
        if self.is_builder:
            return file_class.builder(path=path)
        return file_class(path=path)

    # 3. Mark as a `files` getter to make it retrievable (vs. simple properties)
    setattr(decorator, FILES_CONFIG_KEY, True)

    return decorator
