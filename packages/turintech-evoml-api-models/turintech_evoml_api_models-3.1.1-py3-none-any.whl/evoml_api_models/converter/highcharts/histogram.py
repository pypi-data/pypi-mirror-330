import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class HistogramConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.Histogram) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Fetch constants from graphJson
        add_percent = len(graph_data.data) > 1
        show_gridlines = graph_data.showGridLines

        # Initiate new json
        new_data = dict({"chart": {"type": "column"}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["yAxis"] = hc_data.convert_axis(
            graph_data.yAxis, show_gridlines=show_gridlines
        )
        new_data["xAxis"]["startOnTick"] = False
        new_data["xAxis"]["endOnTick"] = False

        # Fetch data
        histogram_data = [series for series in graph_data.data if series.type == "histogram"]
        line_data = [series for series in graph_data.data if series.type in ["spline", "areaspline"]]
        new_data["series"] = [
            hc_data.convert_histogram_data(series, integer_bins=graph_data.integerBins) for series in histogram_data
        ]

        if add_percent:
            series_sum = np.sum(
                [[point[1] for point in series.data] for series in histogram_data],
                axis=0,
            )
            for series in new_data["series"]:
                for i, point in enumerate(series["data"]):
                    point["percentage"] = (
                        0 if series_sum[i] == 0 else 100 * point["y"] / series_sum[i]
                    )

        new_data["series"].extend(
            [hc_data.convert_line_data(series) for series in line_data]
        )
        if graph_data.maxVisible is not None:
            for i in range(graph_data.maxVisible, len(new_data["series"])):
                new_data["series"][i]["visible"] = False
        # If anomalies given, create anomalies series
        new_data["series"].extend(hc_data.convert_anomalies(graph_data.anomaliesScatter))

        # Construct tooltip info
        histogram_tooltip_dict = graph_data.tooltipKeyDict
        if histogram_tooltip_dict is None:
            histogram_tooltip_dict = {"Count": "{point.y:.0f}"}
            if len(graph_data.data) > 1:
                series_key = graph_data.legendTitle or "Series"
                histogram_tooltip_dict[
                    str(series_key)
                ] = "<span style='color:{point.color}'>●</span> <b>{series.name}</b>"

            if all(series.bins is not None for series in graph_data.data):
                histogram_tooltip_dict["Bin"] = "{point.bin}"

            if add_percent:
                histogram_tooltip_dict["Percentage"] = "{point.percentage:.2f}%"

        histogram_point_format = graph_data.tooltipFormat or \
                                 tooltip.create_tooltip_formatting(
                                     histogram_tooltip_dict, tooltip_as_table
                                 )

        scatter_tooltip_dict = {
            graph_data.xAxis.title or "Value": "<b>{point.x:.2f}</b><br/>"
        }

        scatter_point_format = tooltip.create_tooltip_formatting(scatter_tooltip_dict, tooltip_as_table)
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True, "shared": True}

        # If only one series, disable legend
        if len(new_data["series"]) == 1:
            new_data["legend"]["enabled"] = False

        # Set plot options
        new_data["plotOptions"] = {
            "column": {
                "pointPadding": 0,
                "borderWidth": 1,
                "groupPadding": 0,
                "grouping": False,
                "stickyTracking": True,
                "opacity": 1,
                "tooltip": {"headerFormat": "", "pointFormat": histogram_point_format},
            },
            "scatter": {
                "stickyTracking": True,
                "tooltip": {"headerFormat": "", "pointFormat": scatter_point_format}
            },
            "spline": {
                "stickyTracking": False,
                "tooltip": {"headerFormat": "", "pointFormat": scatter_point_format},
                "marker": {"enabled": False, "symbol": "circle"},
            },
        }

        return new_data


HighchartsConverterFactory.register(GraphType.histogram, HistogramConverter)