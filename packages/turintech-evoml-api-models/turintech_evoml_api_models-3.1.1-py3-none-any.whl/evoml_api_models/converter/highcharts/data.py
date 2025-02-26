from typing import List, Union, Optional

import numpy as np

from ... import graphs
from ... import utils as graph_utils
from . import utils, tooltip


def convert_description(graph: graphs.Graph):
    if graph.description is None:
        return None
    return graph.description.html


def convert_graph_title(graph: graphs.GraphT, default_title: Optional[str] = None, title_key: str = "title"):
    if hasattr(graph, title_key):
        return {"text": getattr(graph, title_key)}
    elif default_title is None:
        return {}
    else:
        return {"text": default_title}


def convert_axis(
        axis: Optional[graph_utils.AxisMetadata],
        show_labels: bool = True,
        show_gridlines: bool = False,
        padding: bool = None,
        convert_name_to_plaintext: bool = True,
) -> dict:
    if axis is None:
        axis_dict = dict()
    else:
        axis_dict = axis.dict()
    if axis_dict.get("title") is not None:
        if convert_name_to_plaintext:
            axis_title = utils.html_to_plaintext(axis_dict["title"])
        else:
            axis_title = axis_dict["title"]
        axis_dict["title"] = {"text": axis_title}
    if not show_labels:
        axis_dict["labels"] = {"enabled": False}
    if not show_gridlines:
        axis_dict["gridLineWidth"] = 0
    if padding is not None:
        axis_dict["maxPadding"] = padding
    return axis_dict


def convert_multiple_axis(axis_list: List[graph_utils.AxisMetadata], **kwargs):
    new_axis_list = [convert_axis(axis, **kwargs) for axis in axis_list]
    number_axis = len(new_axis_list)
    y_axis_width = 100 / number_axis
    for i in range(0, number_axis):
        extra_axis_details = {
            "left": "{p:.2f}%".format(p=i * y_axis_width),
            "width": f"{y_axis_width:.2f}%",
            "showLastLabel": False,
            "offset": 0,
            "lineColor": "#000000",
            "lineWidth": 2,
        }
        new_axis_list[i].update(extra_axis_details)
    return new_axis_list


def common_graph_processing(graph: graphs.GraphT, new_json: dict, default_title: Optional[str] = None):
    # Check for chart size
    chart_size = graph.chartSize
    if chart_size is not None:
        if chart_size[0] is not None:
            new_json["chart"]["height"] = chart_size[0]
        if chart_size[1] is not None:
            new_json["chart"]["width"] = chart_size[1]

    # Check for graph title
    new_json["title"] = convert_graph_title(graph, default_title)
    if graph.subtitle is not None:
        new_json["subtitle"] = {"text": graph.subtitle}

    # Check for legend title
    if hasattr(graph, "legendTitle") and graph.legendTitle is not None:
        new_json["legend"] = {
            "title": {"text": utils.html_to_plaintext(graph.legendTitle)},
            "maxHeight": 80,
        }
    else:
        new_json["legend"] = {"maxHeight": 55}

    return new_json


def convert_bar_data(
    series: graphs.BarChartData, to_percent: bool = False, labels: Optional[List[str]] = None,
        convert_name_to_plaintext: bool = True
):
    assert series.type in ["bar", "column"], "Data must be either bar or column"

    # Convert name to plaintext if applicable
    if convert_name_to_plaintext:
        new_name = utils.html_to_plaintext(str(series.name))
    else:
        new_name = str(series.name)

    all_series_points = []
    if to_percent:
        adjusted_series_data = np.multiply(series.data, 100).tolist()
    else:
        adjusted_series_data = series.data
    for j, point in enumerate(adjusted_series_data):
        new_point = {"x": j, "y": point}
        if labels is not None:
            new_point["x_cat"] = labels[j]
        if series.additionalInfo is not None:
            new_point.update(series.additionalInfo[j])
        all_series_points.append(new_point)
    bar_series = {"name": new_name, "data": all_series_points, "color": series.color, "type": series.type}
    return utils.remove_none_values(bar_series)


def convert_histogram_data(
    series: graphs.HistogramData,
    convert_name_to_plaintext: bool = True,
    integer_bins: bool = False,
):
    if series.type != graphs.GraphDataType.histogram:
        raise ValueError("Series type must be histogram")

    # Convert name to plaintext if applicable
    if convert_name_to_plaintext:
        new_name = utils.html_to_plaintext(str(series.name))
    else:
        new_name = str(series.name)

    # Get list of bin edges
    bins = series.bins
    round_amount = 2

    # Convert data into dictionary form for highcharts
    new_param_data = []
    for i in range(len(series.data)):
        end_bracket = ")" if i < len(series.data) - 1 else "]"
        data_info = {
            "x": series.data[i][0],
            "y": series.data[i][1],
            "bin": f"[{int(bins[i]) if integer_bins else round(bins[i], round_amount)}, "
                   f"{int(bins[i + 1]) if integer_bins else round(bins[i + 1], round_amount)}{end_bracket}",
        }
        new_param_data.append(data_info)

    # Create dictionary for series
    new_series = {"name": new_name, "data": new_param_data, "type": "column"}

    # Show only the first two by default
    # If ordering is given, use that order
    if hasattr(series, "zIndex"):
        new_series["zIndex"] = series.zIndex

    return new_series


def convert_scatter_data(series: graphs.ScatterPlotData, convert_name_to_plaintext: bool = True):
    assert series.type == "scatter", "Series type must be scatter"
    # Convert name to plaintext if applicable
    if convert_name_to_plaintext:
        new_name = utils.html_to_plaintext(str(series.name))
    else:
        new_name = str(series.name)

    series_data = [{"x": point[0], "y": point[1]} for point in series.data]

    if series.additionalInfo is not None:
        for j, point in enumerate(series_data):
            point.update(series.additionalInfo[j])

    new_series = {
        "name": new_name,
        "data": series_data,
        "type": "scatter"
    }

    return new_series


def convert_line_data(
    series: graphs.LineData, labels: Optional[str] = None, convert_name_to_plaintext: bool = True
):
    assert series.type in ["line", "spline", "area", "areaspline"]
    # Convert name to plaintext if applicable
    if convert_name_to_plaintext:
        new_name = utils.html_to_plaintext(str(series.name))
    else:
        new_name = str(series.name)

    series_data = []
    for point in series.data:
        point_data = {"x": point[0], "y": point[1]}
        if labels is not None:
            point_data["x_cat"] = labels[point[0]]
        series_data.append(point_data)
    if series.additionalInfo is not None:
        for j, point in enumerate(series_data):
            point.update(series.additionalInfo[j])

    new_series = {"name": new_name, "data": series_data, "type": series.type,
                  "dashStyle": series.dashStyle, "marker": series.marker,
                  "color": series.color, "seriesDescription": series.seriesDescription,
                  "zIndex": series.zIndex, "visible": series.visible}

    if series.disableTooltip:
        new_series["enableMouseTracking"] = False
    elif series.tooltip:
        new_series["tooltip"] = series.tooltip
    if series.disableLegend:
        new_series["showInLegend"] = False
    return utils.remove_none_values(new_series)


def convert_anomalies(anomalies: Union[graphs.ScatterPlotData, List[graphs.ScatterPlotData]],
                      convert_name_to_plaintext: bool = True):
    if anomalies is None:
        return []
    anomalies_series = []
    if isinstance(anomalies, graphs.ScatterPlotData):
        anomalies = [anomalies]
    for series in anomalies:
        # Convert name to plaintext if applicable
        if convert_name_to_plaintext:
            new_name = utils.html_to_plaintext(str(series.name))
        else:
            new_name = str(series.name)
        if len(series.data) == 0:
            continue

        add_info = series.additionalInfo
        if add_info is not None:
            data = [{"x": point[0], "y": point[1]} for point in series.data]
            for i in range(len(data)):
                data[i].update(add_info[i])
        else:
            data = list(series.data)

        new_series = {
            "name": new_name,
            "data": data,
            "type": series.type,
            "marker": series.marker,
            "visible": False,
        }

        if series.tooltipKeyDict is not None:
            new_series["tooltip"] = {
                "headerFormat": "",
                "pointFormat": tooltip.create_tooltip_formatting(
                    series.tooltipKeyDict, tooltip_as_table=True
                ),
            }

        if series.tooltipFormat is not None:
            new_series["tooltip"] = {
                "headerFormat": "",
                "pointFormat": series.tooltipFormat
            }

        anomalies_series.append(new_series)
    return anomalies_series