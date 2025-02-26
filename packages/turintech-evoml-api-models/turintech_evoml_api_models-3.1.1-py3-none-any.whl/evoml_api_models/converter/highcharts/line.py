from typing import List

import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphDataType, GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class LineConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.LineGraph) -> dict:
        # Declare constants
        tooltip_as_table = True
        allowed_line_types = ["line", "spline", "area", "areaspline"]

        # Fetch constants from graphJson
        line_type = graph_data.lineType.value
        show_gridlines = graph_data.showGridLines
        max_visible = graph_data.maxVisible
        labels = graph_data.labels
        if labels is not None:
            labels = [graph_utils.html_to_plaintext(label) for label in labels]

        # Initiate new json
        new_data = dict({"chart": {"type": line_type}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amounts
        all_x_data = [
            point[0]
            for param in graph_data.data
            for point in param.data
            if param.type in allowed_line_types
        ]
        all_y_data = [
            point[1]
            for param in graph_data.data
            for point in param.data
            if param.type in allowed_line_types
        ]
        x_round_amount = graph_utils.find_appropriate_rounding_amount(all_x_data, allow_scientific=True)
        y_round_amount = graph_utils.find_appropriate_rounding_amount(all_y_data, allow_scientific=True)

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        if labels is not None:
            new_data["xAxis"]["categories"] = labels
        new_data["yAxis"] = hc_data.convert_axis(
            graph_data.yAxis, show_gridlines=show_gridlines
        )
        
        # Fetch data
        new_data["series"] = []
        series_types: List[GraphDataType] = []
        line_series_counter = 0
        for series in graph_data.data:
            series_types.append(series.type)
            if line_type in allowed_line_types:
                new_data["series"].append(hc_data.convert_line_data(series, labels))
                if max_visible is not None and not series.disableTooltip:
                    if line_series_counter >= max_visible:
                        new_data["series"][-1]["visible"] = False
                line_series_counter += 1
            elif series.type == GraphDataType.scatter:
                new_data["series"].append(hc_data.convert_scatter_data(series))
            else:
                raise ValueError(
                    f"Warning: Type {series.type} of series currently not supported "
                )

        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesData))

        # Construct tooltip info
        if len(graph_data.data) > 1:
            line_tooltip_dict = {
                "Series": "<span style='color:{point.color}'>●</span> <b>{series.name}</b>"
            }
        else:
            line_tooltip_dict = {}

        if labels is not None:
            line_tooltip_dict.update(
                {graph_data.xAxis.title or "x": "{point.x_cat}"}
            )
        else:
            line_tooltip_dict.update(
                {
                    graph_data.xAxis.title or "x": f"{graph_utils.round_formatting('point.x', x_round_amount)}"
                }
            )

        line_tooltip_dict.update(
            {
                graph_data.yAxis.title: f"{graph_utils.round_formatting('point.y', y_round_amount)}"
            }
        )

        line_tooltip_dict = graph_data.tooltipKeyDict or line_tooltip_dict

        point_format = graph_data.tooltipFormat or \
                       tooltip.create_tooltip_formatting(line_tooltip_dict, tooltip_as_table)
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        scatter_tooltip_dict = {
            graph_data.yAxis.title or "Value": "<b>{}</b><br/>".format(
                graph_utils.round_formatting("point.y", 3))
        }
        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)

        # Set plot options
        new_data["plotOptions"] = {}
        for series_type in series_types:
            entry = {"tooltip": {"headerFormat": "", "pointFormat": point_format}}
            if series_type != GraphDataType.scatter:
                entry["marker"] = {"enabled": False, "symbol": "circle"}
            new_data["plotOptions"][series_type] = entry

        new_data["plotOptions"]["scatter"] = {
            "tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}
        }

        return new_data


HighchartsConverterFactory.register(GraphType.linePlot, LineConverter)