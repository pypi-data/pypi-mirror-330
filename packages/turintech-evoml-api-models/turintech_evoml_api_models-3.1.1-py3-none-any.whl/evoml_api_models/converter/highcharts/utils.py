import numpy as np

from typing import Any, Union, Callable, Type, Dict, Optional

from pydantic.v1 import BaseModel

from ...graphs import Graph, HighchartsGraph
import collections.abc
from dataclasses import dataclass


@dataclass
class GraphConversionInfo:
    graphModel: Type[BaseModel]
    converter: Callable[[Graph], dict]


def dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def remove_none_values(d):
    if not isinstance(d, collections.abc.Mapping):
        return d
    new_dict = dict()
    for k, v in d.items():
        if isinstance(v, collections.abc.Mapping):
            new_dict[k] = remove_none_values(v)
        elif isinstance(v, list):
            new_dict[k] = [remove_none_values(i) for i in v]
        elif v is not None:
            new_dict[k] = v
    return new_dict


def get_converted_axis_title(axis: dict):
    if axis.get("title") is None:
        return None
    return axis["title"]["text"]


def html_to_plaintext(html_str):
    html_str = html_str.replace("&", "&amp;")
    html_str = html_str.replace('"', "&quot;")
    # html_str = html_str.replace("'", "&#039;")
    html_str = html_str.replace("<", "&lt;")
    html_str = html_str.replace(">", "&gt;")
    # Allow bold
    html_str = html_str.replace("&lt;b&gt;", "<b>")
    html_str = html_str.replace("&lt;/b&gt;", "</b>")
    return html_str


def round_formatting(formatted_value: str, round_amount: int, max_decimals: int = 3):
    if round_amount is None:
        formatting = f"{formatted_value}"
    elif round_amount <= max_decimals:
        formatting = f"{formatted_value}:.{round_amount}f"
    else:
        formatting = f"{formatted_value}:.{max_decimals}f"
    return "{" + formatting + "}"


def find_appropriate_rounding_amount(
    data: np.ndarray, method: str = "diffs", max_decimals: int = 3,
        allow_scientific: bool = True, force_max_decimals: bool = True
):

    if all(abs(np.round(data) - data) < 10e-8):
        return 0

    if allow_scientific and np.quantile(np.abs(data), 0.99) < 0.000001:
        # Only allow if most data is below threshold for scientific notation
        return None

    if force_max_decimals:
        return max_decimals

    if method == "diffs":
        diffs = np.diff(np.sort(data))
        diffs = diffs[diffs != 0]
        if len(diffs) == 0:
            return None
        benchmark = min(diffs)
    elif method == "quantiles":
        quantile = 0.05
        quantile_data = np.quantile(data, np.arange(0, 1 + quantile, quantile))
        diffs = np.diff(quantile_data)
        diffs = diffs[diffs != 0]
        if len(diffs) == 0:
            return None
        benchmark = min(diffs)
    else:
        raise ValueError(f"Method {method} not valid for finding rounding amount.")

    round_amount = max(0, int(-np.floor(np.log10(benchmark))))
    if np.isnan(benchmark):
        return None

    if round_amount <= max_decimals:
        return round_amount
    else:
        return max_decimals