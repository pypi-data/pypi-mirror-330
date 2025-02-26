import numpy as np

from ... import graphs
from . import utils as graph_utils


def add_error_bar(graph: graphs.GraphT, new_data: dict, to_percent: bool = False):
    assert hasattr(graph, "errorBarData")
    assert "series" in new_data
    number_series = len(new_data["series"])
    assert len(graph.errorBarData) == number_series

    error_series = graph.errorBarData
    number_points = sum([len(error_data.data) for error_data in error_series])
    new_error_series = []
    for error_data in error_series:
        data = error_data.data
        if to_percent:
            data = np.multiply(data, 100).tolist()
        new_error_series.append({
                "name": graph_utils.html_to_plaintext(error_data.name),
                "type": "errorbar",
                "data": data
            })
    new_data["series"] = [
        val for pair in zip(new_data["series"], new_error_series) for val in pair
    ]
    error_bar_options = {
        "dashStyle": "Solid",
        "whiskerColor": "#CD5C5C",
        "stemColor": "#CD5C5C",
        "enableMouseTracking": False,
    }
    error_bar_options.update(get_error_bar_variable_options(number_points))
    new_plot_options = {"errorbar": error_bar_options}
    new_data["plotOptions"] = graph_utils.dict_update(
        new_data.get("plotOptions", dict()), new_plot_options
    )
    return new_data


def get_error_bar_variable_options(number_series):
    """Fetch error bar options that change with the
    number of series given"""
    keys = ["whiskerLength", "whiskerWidth", "stemWidth"]
    if number_series == 1:
        values = [16, 4, 4]
    elif 2 <= number_series <= 4:
        values = [8, 2, 2]
    elif 5 <= number_series <= 8:
        values = [6, 2, 2]
    elif 9 >= number_series <= 10:
        values = [5, 1.5, 1.5]
    else:
        values = None

    if values is None:
        return {}

    return {keys[i]: values[i] for i in range(0, len(keys))}