# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from pathlib import Path
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# ──────────────────────────────────────────────────────────────────────────── #
DataT = TypeVar('DataT')

# ---------------------------------------------------------------------------- #
class Writable(Generic[DataT], ABC):
    """A path with an associated write function"""
    path: Path

    @abstractmethod
    def write(self, data: DataT):
        """A write method that writes data to this instance's path"""

class Readable(Generic[DataT], ABC):
    """A path with both a read and write function. The read function has
    additional requirement as it requires a valid, existing path"""

    @abstractmethod
    def read(self) -> DataT:
        """A load method that writes data to this instance's path"""
