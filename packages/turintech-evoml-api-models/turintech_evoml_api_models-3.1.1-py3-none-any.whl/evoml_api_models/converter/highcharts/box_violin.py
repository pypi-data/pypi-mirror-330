import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class BoxViolinPlotConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.BoxViolinPlot) -> dict:
        # Declare constants
        tooltip_as_table = True
        infer_rounding = False

        # Initiate new json
        new_data = dict({"chart": {"type": "areasplinerange", "inverted": True}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amounts
        if graph_data.roundAmount is not None:
            round_amount = graph_data.roundAmount
        elif infer_rounding:
            round_amount = graph_utils.find_appropriate_rounding_amount(
                np.concatenate([[i.min, i.max] for i in graph_data.data_box]),
                allow_scientific=True,
            )
        else:
            round_amount = 3

        # Set axes
        xAxis = hc_data.convert_axis(graph_data.xAxis)
        xAxis["reversed"] = False
        yAxis = hc_data.convert_axis(graph_data.yAxis)
        yAxis["categories"] = [
            graph_utils.html_to_plaintext(params.name) for params in graph_data.data_box
        ]
        yAxis["startOnTick"], yAxis["endOnTick"] = False, False
        xAxis["startOnTick"], xAxis["endOnTick"] = False, False
        yAxis["min"], yAxis["max"] = 0, len(graph_data.data_box) - 1

        new_data["xAxis"] = xAxis
        new_data["yAxis"] = yAxis

        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        # Fetch violin data
        new_data["series"] = []
        violin_data = dict()
        for i, cat in enumerate(graph_data.data_violin):
            violin_data[cat] = [[y_val, -width + i, width + i] for y_val, width in graph_data.data_violin[cat]]

        # Fetch box data
        boxplot_data = []
        mean_scatter_data = []
        # Fetch both the boxplot info and the mean needed for mean scatter
        for i, params in enumerate(graph_data.data_box):
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
                mean_scatter_data.append([params.mean, i])
            boxplot_data.append(new_params)

        # Add violin data
        for i, kde in enumerate(violin_data):
            # Construct tooltip info
            boxplot_tooltip_dict = {
                "Maximum": f"{boxplot_data[i]['high']:.{int(round_amount)}f}",
                "75% Quantile": f"{boxplot_data[i]['q3']:.{int(round_amount)}f}",
                "Median": f"{boxplot_data[i]['median']:.{int(round_amount)}f}",
                "25% Quantile": f"{boxplot_data[i]['q1']:.{int(round_amount)}f}",
                "Minimum": f"{boxplot_data[i]['low']:.{int(round_amount)}f}",
            }

            boxplot_tooltip_format = tooltip.create_tooltip_formatting(
                boxplot_tooltip_dict, tooltip_as_table
            )

            new_data["series"].append({
                "type": "areasplinerange",
                "name": kde,
                "id": str(i),
                "tooltip": {"headerFormat": "", "pointFormat": boxplot_tooltip_format},
                "data": violin_data[kde]
            })

        # Add boxplot data
        for i, box_params in enumerate(boxplot_data):
            # Box (wide line)
            new_data["series"].append({
                "linkedTo": str(i),
                "type": "line",
                "name": "box",
                "marker": {"symbol": "circle", "enabled": False},
                "lineWidth": 8,
                "color": "black",
                "data": [[box_params["q3"], i], [box_params["q1"], i]],
                "enableMouseTracking": False
            })
            # Whiskers (thin line from min to max)
            new_data["series"].append({
                "linkedTo": str(i),
                "type": "line",
                "name": "whiskers",
                "marker": {"symbol": "circle", "enabled": False},
                "lineWidth": 2,
                "color": "black",
                "data": [[box_params["high"], i], [box_params["low"], i]],
                "enableMouseTracking": False
            })
            # Median (white point)
            new_data["series"].append({
                "linkedTo": str(i),
                "type": "scatter",
                "name": "median",
                "marker": {"symbol": "circle"},
                "color": "white",
                "data": [{"x": box_params["median"], "y": i}],
                "enableMouseTracking": False
            })

        # Add mean scatter data
        if len(mean_scatter_data) > 0:
            mean_scatter_tooltip_dict = {"Mean": graph_utils.round_formatting("point.x", round_amount)}
            mean_scatter_tooltip = tooltip.create_tooltip_formatting(
                mean_scatter_tooltip_dict, tooltip_as_table
            )
            new_data["series"].append(
                {
                    "name": "Mean",
                    "stickyTracking": False,
                    "data": mean_scatter_data,
                    "type": "scatter",
                    "marker": {"symbol": "circle"},
                    "visible": False,
                    "color": "#746AB0",
                    "tooltip": {
                        "pointFormat": mean_scatter_tooltip
                        # Mean Scatter has specific formatting separate from anomalies
                    },
                }
            )
        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesData))

        # If anomalies are present adjust their tooltip value to correct axis
        if new_data["series"][-1]["name"] == "Extreme Outliers":
            new_data["series"][-1]["tooltip"]["pointFormat"] = new_data["series"][-1]["tooltip"]["pointFormat"].replace(
                "point.y:.", "point.x:."
            )

        scatter_tooltip_dict = {
            graph_data.yAxis.title or "Value": "<b>{}</b><br/>".format(
                graph_utils.round_formatting("point.x", round_amount))
        }

        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)

        # Set plot options
        new_data["plotOptions"] = {
            "scatter": {
                "tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}
            },
        }

        return new_data


HighchartsConverterFactory.register(GraphType.boxViolinPlot, BoxViolinPlotConverter)
