# ────────────────────────── model related imports ─────────────────────────── #
from typing import List, Tuple, Union, Any, Generic, TypeVar, Optional
from enum import Enum
from pathlib import Path
import json
import re

import numpy as np
from pydantic.v1.generics import GenericModel
from pydantic.v1 import BaseModel

# ──────────────────────────────────────────────────────────────────────────── #
def save_model(model: Union[BaseModel, List[BaseModel]], path: Path):
    """Util to save a pydantic model to a json file. Handles both models and
    lists of models.

    This is the counterpart of 'BaseModel.parse_file' and the utils function
    'parse_file_as' from pydantic.

    Arguments:
        model (Union[BaseModel, List[BaseModel]]):
            A pydantic model, or list of pydantic models, to save to a given
            path.
        path (Path):
            Path where the json should be saved.

    Raises:
        TypeError: if model is not a pydantic model or a list of pydantic models
    """
    json_kwargs = {"indent": 2, "allow_nan": False}
    if isinstance(model, BaseModel):
        path.write_text(model.json(**json_kwargs))
    elif isinstance(model, list):
        # Check that for lists we're given pydantic models as elements
        if not all([isinstance(x, BaseModel) for x in model]):
            raise TypeError("Expected a list of pydantic models")

        with path.open("w") as fobj:
            json.dump([element.dict() for element in model], fobj, **json_kwargs)
    else:
        raise TypeError(f"Unexpected type received {type(model)}")


# ──────────────────────────────────────────────────────────────────────────── #
def update_classwrapper(wrapper, cls):
    """
    When using a decorator, the returned object has its own name and docstring.
    This function allows to update some informations (name, docstring) when
    decorating a class.
    See :func:`functools.update_wrapper` to see the recommended way to achieve
    that result on functions
    """
    for attr in ('__doc__', '__name__'):
        setattr(wrapper, attr, getattr(cls, attr))


# ──────────────────────────────────────────────────────────────────────────── #
def use_alias(original_cls=None, *, generic=None):
    """
    This decorator provides a way to automatically use aliases when saving to a
    dictionary.  Aliases in pydantic are used to load a field (e.g. 'id') from a
    different dictionary key (e.g. '_id').

    Example::
        class Model(BaseModel):
            id: str = Field(..., alias='_id')

    However, there are two issues with defining aliases:
    - When writing back to a dictionary, pydantic uses the model field name
      ('id'), and not the alias ('_id').
    - When recursively loading models, pydantic doesn't recognise the model
      field name ('id') as a valid input to populate 'id': it's expecting to
      populate 'id' using '_id'

    The first issue can be fixed by using the keywork argument 'by_alias=True'
    every time you convert the model to a dictionary.
    This wrappers sets this behaviour (writing to dictionary using the alias) as
    default.

    The second issue can be fixed by providing the Config parameter
    'allow_population_by_field_name = True'
    (see: https://pydantic-docs.helpmanual.io/usage/model_config/)
    This decorator sets that option on every decorated class as well.

    After decoration, we can then:
    - Write to dictionaries using the 'alias' version (_id) by default
    - Load from dictionaries using both the model's name (id) and the alias (_id)
    """
    # For information about optional argument decorators:
    # https://stackoverflow.com/questions/3888158/making-decorators-with-optional-arguments

    def decorate(cls):
        if generic is None:
            # Simple inheritance
            class Wrapped(cls):
                def dict(self, *args, **kwargs):
                    kwargs['by_alias'] = kwargs.get('by_alias', True)
                    return super().dict(*args, **kwargs)
        else:
            # More complex inheritance because it's a generic model
            class Wrapped(cls[generic], Generic[generic]):
                def dict(self, *args, **kwargs):
                    kwargs['by_alias'] = kwargs.get('by_alias', True)
                    return super().dict(*args, **kwargs)

        Wrapped.Config.allow_population_by_field_name = True
        update_classwrapper(Wrapped, cls)

        return Wrapped

    return decorate(original_cls) if original_cls else decorate

# ──────────────────────────────────────────────────────────────────────────── #
def enum_factory(enum_name: str, *strings: Tuple[str]) -> Enum:
    """Factory returning a valid enum class of string type, where each element
    has its own name as value.
    All the elements are given as an arbitrary number of positional arguments

    Args:
        enum_name (str):
            Name of the enum to create
        strings (Tuple[str]):
            Arbitrary number of enum members, that will be given their name as
            value (str)
    Returns: An Enum class containing all the positional arguments as values,
    and named as per the first argument.
    """
    return Enum(enum_name, [(s, s) for s in strings], type=str)


# ──────────────────────────────────────────────────────────────────────────── #
camel_pattern = re.compile(r"(?<!^)(?=[A-Z])")
def to_snake(string: str) -> str:
    return camel_pattern.sub('_', string).lower()


ContentType = TypeVar('ContentType')
class KeyValuePair(GenericModel, Generic[ContentType]):
    name: str
    data: ContentType

def to_highcharts_matrix(arr: List[List[Any]]) -> List[List[Any]]:
    #Transforms an input matrix to a format compatible with highcharts
    grid = np.indices(np.shape(arr))

    row_vals = np.reshape(grid[0],(1,-1))[0]
    col_vals = np.reshape(grid[1],(1,-1))[0]
    vals = np.reshape(arr,(1,-1))[0]
    #In highchart indexing col vals go first
    new_arr = np.transpose([col_vals,row_vals,vals])
    return new_arr.tolist()

def check_dict_list_contains_key(
    kv_list: List[KeyValuePair], keyword: str
) -> List[KeyValuePair]:
    # Check axis metadata contains a title
    key_found = False
    for kv_pair in kv_list:
        if keyword == kv_pair.name:
            key_found = True
    if not key_found:
        raise ValueError(
            'Key value pairs must contain a {0} name e.g. {{"name":{0},"data":<my data>}}'.format(
                keyword
            )
        )
    return kv_list


#Field has to be called weight for highcharts to use
ContentType = TypeVar('ContentType')
class NameWeightPair(GenericModel, Generic[ContentType]):
    name: str
    weight: ContentType

class AxisMetadata(BaseModel):
    #Default no title for the axis. Can be overriden
    title:Optional[str] = ""
    #Default no categories, only placed if some models require it
    type: Optional[str]
    categories:Optional[List[str]]
    min: Optional[float]
    max: Optional[float]
    tickInterval: Optional[float]
    tooltipValueFormat: Optional[str]
    gridLineWidth: Optional[float]
    startOnTick: bool = True
    endOnTick: bool = True

def check_metadata_contains_key(
    metadata: AxisMetadata, keyword: str
) -> AxisMetadata:
    meta_dict = metadata.dict()
    keys = meta_dict.keys()
    if keyword in keys and not meta_dict[keyword] == None:
        return metadata
    else:
        raise ValueError(
            'Key value pairs must contain a {0} name e.g. {{"name":{0},"data":<my data>}}'.format(
                keyword, keyword
            )
        )

__all__ = [
    'KeyValuePair',
]
