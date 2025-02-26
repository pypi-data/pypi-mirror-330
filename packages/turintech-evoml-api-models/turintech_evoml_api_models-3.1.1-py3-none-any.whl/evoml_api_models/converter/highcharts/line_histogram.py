import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory

from math import floor, log10


class LineHistogramConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.LineHistogram) -> dict:
        # Declare constants
        tooltip_as_table = True
        marker_mapping = {
            0: "circle",
            1: "diamond",
            2: "square",
            3: "triangle",
            4: "triangle-down",
        }

        # Fetch constants from graphJson
        show_gridlines = graph_data.showGridLines

        # Initiate new json
        new_data = dict({"chart": {"type": "column"}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amounts
        x_line_data = [
            point[0] for series in graph_data.lineData for point in series.data
        ]
        y_line_data = [
            point[1] for series in graph_data.lineData for point in series.data
        ]

        x_round_amount = graph_utils.find_appropriate_rounding_amount(
            x_line_data, allow_scientific=True
        )
        y_round_amount = graph_utils.find_appropriate_rounding_amount(
            y_line_data, allow_scientific=True
        )

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["xAxis"]["lineWidth"] = 2
        new_data["xAxis"]["startOnTick"] = False
        new_data["xAxis"]["endOnTick"] = False

        new_data["yAxis"] = [hc_data.convert_axis(axis) for axis in graph_data.yAxis]
        for i in new_data["yAxis"]:
            i["lineWidth"] = 2
            i["showEmpty"] = False

        if len(new_data["yAxis"]) > 1:
            new_data["yAxis"][1]["opposite"] = True
            if show_gridlines:
                new_data["yAxis"]["gridLineWidth"] = 0

        # Finding the number after decimal points that we want to have for the
        # y-axis labels of Density (KDE).
        # Maximum value of kde:
        kde_peak = max(graph_data.lineData[0].data, key=lambda x: x[1])[1]
        # Points after decimal 'x': peak/100 < 10^-x < peak/10
        # thus: 2 - log10(peak) > x > 1 - log10(peak)
        # And if x > 1 - log10(peak)
        # This is same as x = ceil(1 - log10(peak)) = 1 - floor(log10(peak))
        new_data["yAxis"][0]["labels"] = {
            "format": f"{{value:.{max(1 - floor(log10(kde_peak)), 0)}f}}"
        }

        # Fetch histogram data
        new_data["series"] = [
            hc_data.convert_histogram_data(
                series, integer_bins=graph_data.integerBins
            ) for series in graph_data.histogramData
        ]

        extra_histogram_info = {
            "type": "column",
            "yAxis": 1 if len(graph_data.yAxis) > 1 else 0,
        }

        for series in new_data["series"]:
            series.update(extra_histogram_info)

        # Fetch line data
        for i, series in enumerate(graph_data.lineData):
            new_param = hc_data.convert_line_data(series)
            new_param["yAxis"] = 0
            new_param["marker"] = {"symbol": marker_mapping[i % 5], "radius": 0}

            if graph_data.maxVisible is not None and i >= graph_data.maxVisible:
                new_param["visible"] = False

            new_data["series"].append(new_param)

        # If anomalies given, create anomalies series
        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesScatter))

        # Construct tooltip info
        if all(series.bins is not None for series in graph_data.histogramData):
            histogram_tooltip_dict = {"Bin": "{point.bin}", "Count": "{point.y:.0f}"}
        else:
            histogram_tooltip_dict = {"Count": "{point.y:.0f}"}

        line_tooltip_dict = {
            f"{graph_data.xAxis.title}": graph_utils.round_formatting(
                "point.x", x_round_amount
            ),
            f"{graph_data.yAxis[0].title}": graph_utils.round_formatting(
                "point.y", y_round_amount
            ),
        }

        histogram_point_format = tooltip.create_tooltip_formatting(
            histogram_tooltip_dict, tooltip_as_table
        )
        line_point_format = tooltip.create_tooltip_formatting(line_tooltip_dict, tooltip_as_table)

        # Note that "shared" attribute in combination with "stickyTracking" in
        # plotOptions allows us to "prioritise" tooltips of specific series.
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True, "shared": True}

        scatter_tooltip_dict = {
            graph_data.xAxis.title or "Value": "<b>{point.x:.2f}</b><br/>"
        }
        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)

        # For histogram's columns we have to specify bin width manually due to
        # the nature of how Highcharts works with multiple series on one axis.
        # Particularly, the width of columns is adjusted taking the KDE line
        # points into account and width between them. Since all bins are of the
        # same width we can simply use the first point's information.
        first_point_bins = graph_data.histogramData[0].bins
        bin_width = first_point_bins[1] - first_point_bins[0]

        # Set plot options
        new_data["plotOptions"] = {
            "spline": {
                "stickyTracking": False,
                "marker": {"enabled": True},
                "tooltip": {
                    "headerFormat": "",
                    "pointFormat": line_point_format,
                },
            },
            "column": {
                "pointPadding": 0,
                "borderWidth": 1,
                "groupPadding": 0,
                "pointRange": bin_width,
                "grouping": False,
                "stickyTracking": True,
                "tooltip": {"headerFormat": "", "pointFormat": histogram_point_format},
            },
            "scatter": {
                "stickyTracking": True,
                "tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}
            },
        }

        return new_data


HighchartsConverterFactory.register(GraphType.lineHistogram, LineHistogramConverter)
