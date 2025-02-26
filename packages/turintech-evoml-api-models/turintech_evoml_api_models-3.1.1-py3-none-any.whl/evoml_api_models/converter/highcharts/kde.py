import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip


from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory

from math import floor, log10

class KDEConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.KDE) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Fetch constants from graphJson
        show_gridlines = graph_data.showGridLines
        graph_type = "areaspline" if graph_data.shadeArea else "spline"

        # Initiate new json
        new_data = dict({"chart": {"type": graph_type}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amounts
        x_round_amount = graph_utils.find_appropriate_rounding_amount(
            [point[0] for param in graph_data.data for point in param.data],
            allow_scientific=True,
        )

        y_round_amount = graph_utils.find_appropriate_rounding_amount(
            [point[1] for param in graph_data.data for point in param.data],
            allow_scientific=True,
        )

        # Set axes
        yAxis = hc_data.convert_axis(graph_data.yAxis, show_gridlines=show_gridlines)
        yAxis["min"] = 0
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["yAxis"] = yAxis

        # Finding the number after decimal points that we want to have for the
        # y-axis labels of Density.
        # Maximum value of kde:
        kde_peak = max([i[1] for i in graph_data.data[0].data])
        # Points after decimal 'x': peak/100 < 10^-x < peak/10
        # thus: 2 - log10(peak) > x > 1 - log10(peak)
        # And if x > 1 - log10(peak)
        # This is same as x = ceil(1 - log10(peak)) = 1 - floor(log10(peak))
        new_data["yAxis"]["labels"] = {
            "format": f"{{value:.{max(1 - floor(log10(kde_peak)), 0)}f}}"
        }

        # Fetch data
        new_data["series"] = [hc_data.convert_line_data(series) for series in graph_data.data]
        if graph_data.maxVisible is not None:
            for i, series in enumerate(new_data["series"]):
                if i >= graph_data.maxVisible:
                    series["visible"] = False

        # Fetch anomalies if they exist
        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesScatter))

        # Disable legend if only 1 entry
        if len(new_data["series"]) == 1:
            new_data["legend"]["enabled"] = False

        # Construct tooltip info
        if len(new_data["series"]) > 1:
            series_key = graph_data.legendTitle or "Series"
            kde_tooltip_dict = {
                f"{series_key}": "<span style='color:{point.color}'>●</span> <b>{series.name}</b>"
            }
        else:
            kde_tooltip_dict = {}

        kde_tooltip_dict.update(
            {
                f"{graph_data.xAxis.title}": graph_utils.round_formatting(
                    "point.x", x_round_amount
                ),
                f"{graph_data.yAxis.title}": graph_utils.round_formatting(
                    "point.y", y_round_amount
                ),
            }
        )

        scatter_tooltip_dict = {
            graph_data.xAxis.title or "Value": "<b>{point.x:.2f}</b><br/>"
        }

        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)

        kde_tooltip_format = graph_data.tooltipFormat or \
                             tooltip.create_tooltip_formatting(kde_tooltip_dict, tooltip_as_table)
        extra_tooltip_info = {}
        if tooltip_as_table:
            extra_tooltip_info["useHTML"] = True
        if graph_data.sharedTooltip:
            extra_tooltip_info["shared"] = True
        if len(extra_tooltip_info) > 0:
            new_data["tooltip"] = extra_tooltip_info

        # Set plot options
        new_data["plotOptions"] = {
            graph_type: {
                "fillOpacity": 0.1,
                "marker": {"enabled": False, "symbol": "circle"},
                "tooltip": {
                    "headerFormat": graph_data.tooltipHeaderFormat or "",
                    "pointFormat": kde_tooltip_format,
                },
            },
            "scatter": {
                "tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}
            },
        }

        return new_data


HighchartsConverterFactory.register(GraphType.KDE, KDEConverter)