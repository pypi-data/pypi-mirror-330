"""This module provides a Pattern class that declares an output contract:
a given application can explain which files will be generated using patterns
(linux glob, regex, or any function) to help the consumer figure out, for
a given file, which type of output it is and how to load it.
"""
# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import (
    TypeVar,
    Type,
    Dict,
    Union,
    Generic,
    Optional,
    Callable,
    Any,
    Generator,
)
from fnmatch import fnmatch
from pathlib import Path
from functools import partial
import inspect
import logging
import re

# Dependencies
from pydantic.v1 import BaseModel, validator
from pydantic.v1.generics import GenericModel

# Module
from .files import File
from .folder import is_partial_subclass

# ──────────────────────────────────────────────────────────────────────────── #
# Generic Types
K = TypeVar('K')  # pylint: disable=C0103
V = TypeVar('V')  # pylint: disable=C0103
ODict = Optional[Dict[K, V]]

# ──────────────────────────────────────────────────────────────────────────── #
PathChecker = Callable[[Path], bool]
FileT = TypeVar('FileT', bound=File)

logger = logging.getLogger("models.tests_io")
logger.setLevel(logging.DEBUG)


class Pattern(BaseModel):
    """This class provides an object that helps you check if a path follows
    a given pattern. The pattern can be any arbitrary check on a Path, with
    convenience methods for regex & glob based checks.

    It also provides the ability to easily go over all valid files in a folder.
    """
    is_valid: PathChecker

    def iterdir(self, directory: Path) -> Generator[FileT, None, None]:
        """Creates instances of fileTYpe for all valid instances found in the
        given directory (validates whether or not a given directory respects the
        contract expressed by this pattern instance)
        """
        for path in directory.iterdir():
            if self.is_valid(path):
                yield path

    @staticmethod
    def from_regex(regex_str: str, root: Optional[Path] = None) -> PathChecker:
        """Provide an easy 'is_valid' pattern function that checks if the
        (absolute) path matches a given regex.

        To simplify the regex, you might provide a root to get a relative path
        instead (e.g. have a regex only on 'my_script.py' instead of
        'my/workdir/folder/my_script.py')
        """
        regex = re.compile(regex_str)

        def is_valid(path: Path) -> bool:
            path_str = str(path.relative_to(root) if root is not None else path)
            match = regex.search(path_str)
            # logger.debug("--- path: %s", path)
            # logger.debug("%s", match)
            return match is not None

        return is_valid

    @staticmethod
    def from_glob(glob: str, root: Optional[Path] = None) -> PathChecker:
        """Provide an easy 'is_valid' pattern function that checks if the
        (absolute) path matches a linux glob pattern

        To simplify the regex, you might provide a root to get a relative path
        instead (e.g. have a regex only on 'my_script.py' instead of
        'my/workdir/folder/my_script.py')
        """

        def is_valid(path: Path) -> bool:
            path_str = str(path.relative_to(root) if root is not None else path)
            return fnmatch(path_str, glob)

        return is_valid


# ──────────────────────────────────────────────────────────────────────────── #
T = TypeVar('T')  # pylint: disable=C0103
PType = Union[Type[T], Any]
class FactoryPattern(GenericModel, Generic[FileT], Pattern):
    """Adds to the Pattern class the ability to create instances of a given File
    subclass for paths that follow the defined pattern.

    The provided subclass `file_type` should take as only required argument the
    `path` field. You can use `functools.partial` to define such a subclass from
    more complicated classes (see examples).

    The generic `FileT` is here for type hints only, and allows to type the
    factory methods (returning instances of `file_type`). `FileT` should be equal
    to `file_type`, although at runtime only `file_type` matters.

    Examples:

        from functools import partial
        is_config = Pattern.from_glob("config_*.json")
        config_pattern = FactoryPattern(
            is_valid=is_config, file_type=JsonFile.with_model(Config)
        )

    The sample above defines on the fly a subclass of JsonFile that only works
    for json files loadable with the Config model.
    """
    file_type: PType[File]

    @validator('file_type')
    def only_path_required(cls, file_type: Type[File]):
        """Checks that the only required field is `path`"""
        required = []
        for parameter in inspect.signature(file_type).parameters.values():
            if (
                parameter.default == inspect.Parameter.empty
                and parameter.name != "args"
            ):
                required.append(parameter.name)

        expected = ["path"]
        if required != expected:
            raise ValueError(
                "FactoryPattern's file_type required arguments: "
                f"expected={expected}, found={required}"
            )
        return file_type

    @validator('file_type')
    def partial_or_file(cls, file_type: Union[Type[File], partial]):
        """Checks that `file_type` is either a subclass of File or a partial
        subclass of File
        """
        if not is_partial_subclass(file_type, File):
            raise ValueError(
                f"provided class is {file_type}, expected a subclass of {File}"
            )
        return file_type

    def create(self, path: Path) -> FileT:
        """Creates an instance of file_type using the given path and the set
        defaults (that are validated to include any other required argument)
        """
        return self.file_type(path=path)

    def files(self, directory: Path):
        """For every valid file in the given directory, yields an instance of
        `file_type`
        """
        for path in self.iterdir(directory):
            yield self.create(path)
