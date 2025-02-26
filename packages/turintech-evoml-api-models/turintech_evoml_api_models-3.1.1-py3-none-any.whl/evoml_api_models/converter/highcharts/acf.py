"""Module providing code for users to create autocorrelation function plot."""
# ───────────────────────────────── Imports ────────────────────────────────── #

# Standard Library
# 3rd Party

# Private
from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip
from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class ACFConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.ACFPlot) -> dict:
        """Converting a graph to output a json for autocorrelation plot (including confidence intervals).
        Args:
            graph_data (Graph[graphs.ACFPlot]):
                Graph Model containing the necessary information to
                create a lollipop + area chart.
        Returns:
            new_data (dict):
                Json dictionary that follows this style:
                https://www.highcharts.com/demo/lollipop
                https://www.highcharts.com/demo/arearange-line
        """

        # Initiate new json
        new_data = {"chart": {"type": "lollipop"}}
        new_data = hc_data.common_graph_processing(graph_data, new_data)
        # Set axes and tooltip
        new_data["xAxis"] = {"type": "category"}
        new_data["yAxis"] = {"gridLineWidth": 1}
        # Create x-axis and y-axis title
        if graph_data.xAxis.title:
            new_data["xAxis"]["title"] = {
                "text": graph_utils.html_to_plaintext(graph_data.xAxis.title)
            }
        if graph_data.yAxis.title:
            new_data["yAxis"]["title"] = {
                "text": graph_utils.html_to_plaintext(graph_data.yAxis.title)
            }
        # Add remaining fields for y-axis
        for key, item in graph_data.yAxis:
            # Skip adding title
            if key in new_data["yAxis"]:
                continue
            else:
                new_data["yAxis"][key] = item
        # Fetch data
        new_data["series"] = []
        # Assume data is already in list of lists (otherwise adapt construction)
        for points in graph_data.data:
            # The confidence interval has its own features so needs to be added separately
            if len(points) > 3:
                dataset = points
            else:
                dataset = {"name": points["name"], "data": points["data"]}
            new_data["series"].append(dataset)
        # Create tooltip information
        new_data["tooltip"] = {"useHTML": True,
                               "shared": True}
        # Add plot options
        new_data["plotOptions"] = {
            "lollipop": {
                "tooltip": {
                    "headerFormat": "Lag {point.x} <br><br>",
                    "pointFormat": graph_data.plotOptions["lollipop"],

                }
            },
            "arearange": {
                "marker": {"enabled": False},
                "showInLegend": False,
                "lineWidth": 1,
                "fillOpacity": 0.1,
                "tooltip": {
                    "headerFormat": "Lag {point.x} <br><br>",
                    "pointFormat": graph_data.plotOptions["arearange"],
                },
            },
        }
        # Return data
        return new_data


HighchartsConverterFactory.register(GraphType.acfPlot, ACFConverter)
