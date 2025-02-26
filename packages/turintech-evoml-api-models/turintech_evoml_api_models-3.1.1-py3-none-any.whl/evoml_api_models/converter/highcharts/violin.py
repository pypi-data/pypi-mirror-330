import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class ViolinPlotConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.ViolinPlot) -> dict:
        # Declare constants
        tooltip_as_table = True
        infer_rounding = False

        # Initiate new json
        new_data = dict({"chart": {"type": "areasplinerange", "inverted": False}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        xAxis = hc_data.convert_axis(graph_data.xAxis)
        xAxis["reversed"] = False
        yAxis = hc_data.convert_axis(graph_data.yAxis)
        new_data["xAxis"] = xAxis
        new_data["yAxis"] = yAxis

        # Converting data:
        # data is a dictionary of lists of numeric values.
        data = graph_data.data

        # Each inner list contains 3 parameters: the value itself, width to
        # the left, width to the right. Two widths must be identical as the
        # violin plot is symmetrical.
        violin_data = [[x, -y, y] for x, y in zip(*data["Violin_points"])]

        new_data["series"] = [
            {"name": graph_data.columnName, "data": violin_data, "showInLegend": False, "softThreshold": False}
        ]

        # Checking whether to also plot median, lower and upper quantile lines
        if graph_data.showMedianLine:
            if data["Mean"]:
                mean_scatter_tooltip_dict = {"Mean": graph_utils.round_formatting("point.x", 2)}
                mean_scatter_tooltip = tooltip.create_tooltip_formatting(mean_scatter_tooltip_dict, tooltip_as_table)
                new_data["series"].append(
                    {
                        "name": "Mean",
                        "stickyTracking": False,
                        "type": "scatter",
                        "marker": {"radius": 5, "symbol": "circle"},
                        "visible": True,
                        "color": "#1d1145",
                        "data": [[data["Mean"][0], 0]],
                        "tooltip": {"pointFormat": mean_scatter_tooltip},
                    }
                )
            for metric in ("25th Quantile", "Median", "75th Quantile"):
                if data[metric]:
                    new_data["series"].append(
                        {
                            "name": metric,
                            "type": "line",
                            "color": "#1d1145",
                            "visible": True,
                            "data": [[data[metric][0], -data[metric][1]], [data[metric][0], data[metric][1]]],
                            "marker": False,
                            "enableMouseTracking": False,  # Disables the tooltip
                        }
                    )

        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesData))

        violin_tooltip_dict = {
            "Minimum": data["MinMax"][0],
            "25th Quantile": data["25th Quantile"][0],
            "Median": data["Median"][0],
            "75th Quantile": data["75th Quantile"][0],
            "Maximum": data["MinMax"][1],
        }

        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        round_amount = 3

        scatter_tooltip_dict = {
            graph_data.yAxis.title
            or "Value": "<b>{}</b><br/>".format(graph_utils.round_formatting("point.y", round_amount))
        }

        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)

        violin_tooltip_format = tooltip.create_tooltip_formatting(violin_tooltip_dict, tooltip_as_table)
        # Set plot options
        new_data["plotOptions"] = {
            # Note: the `distance` parameter is set to a large value because it
            # is the only known way to prevent the tooltip from moving.
            "areasplinerange": {
                "tooltip": {"headerFormat": "", "pointFormat": violin_tooltip_format, "distance": 10000},
                "fillColor": "#ebf3fe",
                "marker": False,
            },
            "scatter": {"tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}},
        }

        return new_data


HighchartsConverterFactory.register(GraphType.violinPlot, ViolinPlotConverter)
