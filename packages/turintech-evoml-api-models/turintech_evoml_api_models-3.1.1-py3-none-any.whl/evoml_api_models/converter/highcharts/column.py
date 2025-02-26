import numpy as np

from ... import graphs
from ...utils import to_highcharts_matrix
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class ColumnChartConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.ColumnChart) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Fetch constants from graphJson
        show_gridlines = graph_data.showGridLines
        stacking = graph_data.stacking
        inverted = graph_data.inverted

        # Initiate new json
        new_data = dict({"chart": {"type": "column"}})
        if inverted:
            new_data["chart"]["inverted"] = True

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["xAxis"]["categories"] = [
            graph_utils.html_to_plaintext(label) for label in graph_data.labels
        ]
        new_data["yAxis"] = hc_data.convert_axis(
            graph_data.yAxis, show_gridlines=show_gridlines
        )
        if stacking == "percent":
            new_data["yAxis"]["labels"] = {"format": "{value}%"}
        elif stacking is None:
            new_data["yAxis"]["labels"] = {"enabled": False}
            new_data["yAxis"]["gridLineWidth"] = 0
            new_data["yAxis"]["maxPadding"] = 0.25

        # Fetch data
        new_data["series"] = [
            hc_data.convert_bar_data(series, labels=new_data["xAxis"]["categories"])
            for series in graph_data.data
        ]

        # Set visible to maxVisible if it exists
        if graph_data.maxVisible is not None:
            for i in range(graph_data.maxVisible, len(new_data["series"])):
                new_data["series"][i]["visible"] = False

        # Construct tooltip info
        if graph_data.tooltipKeyDict is not None:
            column_tooltip_dict = graph_data.tooltipKeyDict
        elif stacking == "percent":
            column_tooltip_dict = {
                "Series": "<span style='color:{point.color}'>●</span> <b>{series.name}</b>",
                "Label": "{point.x_cat}",
                "Count": "{point.y:.0f}",
                "Percentage": "{point.percentage:.2f}%",
            }
        else:
            column_tooltip_dict = {
                "Series": "<span style='color:{point.color}'>●</span> <b>{series.name}</b>",
                "Label": "{point.x_cat}",
                "Count": "{point.y:.0f}",
            }

        column_tooltip_format = graph_data.tooltipFormat or tooltip.create_tooltip_formatting(
            column_tooltip_dict, tooltip_as_table
        )
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        # Set plot options
        new_data["plotOptions"] = {"column": {"stacking": stacking}}
        if stacking == "percent":
            new_plot_options = {
                "column": {
                    "tooltip": {"headerFormat": "", "pointFormat": column_tooltip_format}
                }
            }
            new_data["plotOptions"] = graph_utils.dict_update(new_data["plotOptions"], new_plot_options)
        elif stacking is None:
            new_plot_options = {
                "column": {
                    "minPointLength": 2,
                    "groupPadding": 0.075,
                    "pointPadding": 0.05,
                    "dataLabels": {
                        "enabled": True,
                        "style": {"fontSize": "14px"},
                        "allowOverlap": True,
                    },
                    "tooltip": {
                        "headerFormat": "",
                        "pointFormat": column_tooltip_format,
                    },
                }
            }
            new_data["plotOptions"] = graph_utils.dict_update(new_data["plotOptions"], new_plot_options)

        return new_data


HighchartsConverterFactory.register(GraphType.columnChart, ColumnChartConverter)