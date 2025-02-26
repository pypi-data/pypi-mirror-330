# ───────────────────────────────── imports ────────────────────────────────── #
from typing import List, Optional

from pydantic.v1 import Field

from evoml_api_models.base.base_data_types import BaseModelWithAlias
from evoml_api_models.optimisation import DatasetMetadata

# ──────────────────────────────────────────────────────────────────────────── #
#      specifies all modules that shall be loaded and imported into the        #
#      current namespace when us use from package import *                     #
# ──────────────────────────────────────────────────────────────────────────── #

__all__ = ['DatasetFileHeaders', 'DatasetConfig']


# ──────────────────────────────────────────────────────────────────────────── #
#                           EvomlWorker Data Models                            #
# ──────────────────────────────────────────────────────────────────────────── #


class DatasetFileHeaders(BaseModelWithAlias):
    """
    Data structure with the information of headers
    """
    original_headers: Optional[List[str]]
    cleaned_headers: Optional[List[str]]


class DatasetConfig(DatasetFileHeaders):
    """
    Configuration obtained in EvomlWorker.download_dataset method
    """
    metadata: Optional[DatasetMetadata] = Field(
        None,
        description="Information about the dataset downloaded from enigma's "
                    "database"
    )
