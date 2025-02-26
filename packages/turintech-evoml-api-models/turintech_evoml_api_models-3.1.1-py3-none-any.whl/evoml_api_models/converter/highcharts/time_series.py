import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class TimeSeriesConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.LineGraph) -> dict:
        """Converting a graph to output a json for time series.

        Args:
            graph_data (Graph[graphs.LineGraph]):
                Graph Model containing the necessary information to
                create a time series line-chart.

        Returns:
            new_data (dict):
                Json dictionary that follows this style:
                https://www.highcharts.com/demo/spline-irregular-time.
        """
        # Initiate new json
        new_data = {"chart": {"type": graph_data.lineType.value}}
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Set axes
        new_data["xAxis"] = {"type": graph_data.xAxis.type,
                             "min": None if graph_data.xAxis.min is None else graph_data.xAxis.min,
                             "max": None if graph_data.xAxis.max is None else graph_data.xAxis.max,
                             "startOnTick": False if graph_data.xAxis.type is None else True,
                             "endOnTick": True if graph_data.xAxis.type is None else False}
        new_data["yAxis"] = {"gridLineWidth": 1}

        if graph_data.xAxis.title:  # not None, not empty
            new_data["xAxis"]["title"] = {
                "text": graph_utils.html_to_plaintext(graph_data.xAxis.title)
            }

        if graph_data.yAxis.title:  # not None, not empty
            new_data["yAxis"]["title"] = {
                "text": graph_utils.html_to_plaintext(graph_data.yAxis.title)
            }

        # Fetch data
        new_data["series"] = []
        line_series_counter = 0
        for points in graph_data.data:
            dataset = {
                "name": points.name,
                "data": [list(elem) for elem in points.data],
                "dashStyle": points.dashStyle,
                "showInLegend": not points.disableLegend,
                "visible": points.visible
            }
            if points.color:
                dataset["color"] = points.color
            if graph_data.maxVisible is not None and not points.disableTooltip:
                if line_series_counter >= graph_data.maxVisible:
                    new_data["series"][-1]["visible"] = False
                line_series_counter += 1
            new_data["series"].append(dataset)

        # Set general tooltip and plot options
        new_data["tooltip"] = {"xDateFormat": "%Y-%m-%d (%A)", "useHTML": True, "shared": True}
        if not graph_data.plotOptions:
            new_data["plotOptions"] = {"line": {"tooltip":
                                                    {"pointFormat": graph_data.tooltipFormat},
                                                "marker":
                                                    {"enabled": False}
                                                }
                                       }
        else:
            new_data["plotOptions"] = graph_data.plotOptions
        return new_data


HighchartsConverterFactory.register(GraphType.timeseriesLineChart, TimeSeriesConverter)
