import numpy as np

from typing import Dict

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class BoxPlotConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.BoxPlot) -> dict:
        # Declare constants
        tooltip_as_table = True
        infer_rounding = False

        # Initiate new json
        new_data = dict({"chart": {"type": "boxplot", "inverted": True}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amounts
        if graph_data.roundAmount is not None:
            round_amount = graph_data.roundAmount
        elif infer_rounding:
            round_amount = graph_utils.find_appropriate_rounding_amount(
                np.concatenate([[i.min, i.max] for i in graph_data.data]),
                allow_scientific=True,
            )
        else:
            round_amount = 3

        # Set axes
        xAxis = hc_data.convert_axis(graph_data.xAxis)
        xAxis["categories"] = [graph_utils.html_to_plaintext(params.name) for params in graph_data.data]
        yAxis = hc_data.convert_axis(graph_data.yAxis)

        if graph_data.showMeanLine and graph_data.overallMean is not None:
            total_mean = graph_data.overallMean
            plot_lines = [{"value": total_mean, "color": "red", "width": 1, "zIndex": 20}]
            yAxis["plotLines"] = plot_lines

        new_data["xAxis"] = xAxis
        new_data["yAxis"] = yAxis

        # If single column then vertical axis is irrelevant so disabling it
        if new_data["xAxis"]["title"] is None:
            new_data["xAxis"]["visible"] = False

        if graph_data.datetime_tooltip:
            new_data["yAxis"]["labels"] = {"format": f"{{value:{graph_data.datetime_tooltip}}}"}

        # Fetch data
        boxplot_data = []
        mean_scatter_data = []
        # Fetch both the boxplot info and the mean needed for mean scatter
        for i, params in enumerate(graph_data.data):
            new_params = {
                "low": params.min,
                "q1": params.lower_quartile,
                "median": params.median,
                "q3": params.upper_quartile,
                "high": params.max,
            }
            if new_params["q1"] == new_params["median"] or new_params["q3"] == new_params["median"]:
                new_params["medianWidth"] = 2.5
            if graph_data.showMeanScatter:
                mean_scatter_data.append([i, params.mean])
            boxplot_data.append(new_params)

        # Add boxplot data
        new_data["series"] = [
            {
                "name": "boxplot",
                "data": boxplot_data,
                "softThreshold": False,
                "showInLegend": False,
            }
        ]

        # Add mean scatter data
        if mean_scatter_data:
            mean_round_amount = 0 if all(round(i[1]) == i[1] for i in mean_scatter_data) else 2
            mean_scatter_tooltip_dict: Dict[str, str] = {
                "Mean": graph_utils.round_formatting("point.y", mean_round_amount)
            }
            if graph_data.datetime_tooltip:
                mean_scatter_tooltip_dict["Mean"] = mean_scatter_tooltip_dict["Mean"].replace(
                    f".{mean_round_amount}f", graph_data.datetime_tooltip
                )
            mean_scatter_tooltip = tooltip.create_tooltip_formatting(mean_scatter_tooltip_dict, tooltip_as_table)
            new_data["series"].append(
                {
                    "name": "Mean",
                    "stickyTracking": False,
                    "data": mean_scatter_data,
                    "type": "scatter",
                    "marker": {"radius": 5},
                    "visible": False,
                    "color": "#1d1145",
                    "tooltip": {
                        "pointFormat": mean_scatter_tooltip
                        # Mean Scatter has specific formatting separate from anomalies
                    },
                }
            )
        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesData))

        # Construct tooltip info
        boxplot_tooltip_dict = {
            "Minimum": graph_utils.round_formatting("point.low", round_amount),
            "25% Quantile": graph_utils.round_formatting("point.q1", round_amount),
            "Median": graph_utils.round_formatting("point.median", round_amount),
            "75% Quantile": graph_utils.round_formatting("point.q3", round_amount),
            "Maximum": graph_utils.round_formatting("point.high", round_amount),
        }

        if graph_data.datetime_tooltip:
            for key, value in boxplot_tooltip_dict.items():
                boxplot_tooltip_dict[key] = value.replace(f".{round_amount}f", graph_data.datetime_tooltip)

        boxplot_tooltip_format = tooltip.create_tooltip_formatting(boxplot_tooltip_dict, tooltip_as_table)
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        scatter_tooltip_dict = {
            graph_data.yAxis.title or "Value": f'<b>{graph_utils.round_formatting("point.y", round_amount)}</b><br/>'
        }

        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)
        if graph_data.datetime_tooltip:
            scatter_point_format = scatter_point_format.replace(f".{round_amount}f", graph_data.datetime_tooltip)

        # Set plot options
        new_data["plotOptions"] = {
            "boxplot": {
                "tooltip": {"headerFormat": "", "pointFormat": boxplot_tooltip_format},
                "stemDashStyle": "Dot",
                "stemColor": "#ff851b",
                "whiskerColor": "#34bfa3",
                "fillColor": "#ebf3fe",
            },
            "scatter": {"tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}},
        }

        return new_data


HighchartsConverterFactory.register(GraphType.boxPlot, BoxPlotConverter)
