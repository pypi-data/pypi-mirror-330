import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class ScatterPlotConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.ScatterPlot) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Initiate new json
        new_data = dict({"chart": {"type": "scatter"}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amounts
        x_round_amount = graph_utils.find_appropriate_rounding_amount(
            [
                point[0]
                for param in graph_data.data
                for point in param.data
                if param.type == "scatter"
            ],
            method="quantiles",
            allow_scientific=True,
        )
        y_round_amount = graph_utils.find_appropriate_rounding_amount(
            [
                point[1]
                for param in graph_data.data
                for point in param.data
                if param.type == "scatter"
            ],
            method="quantiles",
            allow_scientific=True,
        )

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["yAxis"] = hc_data.convert_axis(graph_data.yAxis)

        # Fetch data
        new_data["series"] = []
        for param in graph_data.data:
            series_type = param.type
            if series_type is None or series_type == "scatter":
                new_param = hc_data.convert_scatter_data(param)
            elif series_type == "line":
                new_param = hc_data.convert_line_data(
                    param, convert_name_to_plaintext=False
                )
            else:
                raise ValueError(
                    f"Warning: Type {series_type} of series currently not supported "
                )
            new_data["series"].append(new_param)
        # Add anomalies
        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesData))

        # Construct tooltip info
        scatter_tooltip_dict = {
            graph_data.xAxis.title
            or "x": graph_utils.round_formatting("point.x", x_round_amount),
            graph_data.yAxis.title
            or "y": graph_utils.round_formatting("point.y", y_round_amount),
        }
        scatter_tooltip_dict = graph_data.tooltipKeyDict or scatter_tooltip_dict

        scatter_tooltip_format = (
            graph_data.tooltipFormat
            or tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)
        )
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        # Update legend to use HTML
        new_data["legend"] = graph_utils.dict_update(
            new_data.get("legend", dict()), {"useHTML": True}
        )

        # Set plot options
        new_data["plotOptions"] = {
            "scatter": {
                "tooltip": {
                    "headerFormat": "{point.x:%Y-%m-%d (%A)}"
                    if graph_data.xAxis.type == "datetime"
                    else "",
                    "pointFormat": scatter_tooltip_format,
                }
            },
            "line": {
                "marker": {"enabled": False, "symbol": "circle"},
                "tooltip": {
                    "headerFormat": "",
                    "pointFormat": "{series.userOptions.seriesDescription}",
                },
            },
        }

        return new_data


HighchartsConverterFactory.register(GraphType.scatterPlot, ScatterPlotConverter)
