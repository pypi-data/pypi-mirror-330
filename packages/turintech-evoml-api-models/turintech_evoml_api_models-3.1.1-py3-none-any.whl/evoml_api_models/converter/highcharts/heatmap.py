import numpy as np

from ... import graphs
from ...utils import to_highcharts_matrix
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class HeatMapConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.HeatMap):
        # Declare constants
        tooltip_as_table = True

        # Fetch constants from graphJson
        additional_info = graph_data.additionalInfo

        # Initiate new json
        new_data = dict({"chart": {"type": "heatmap"}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amount
        round_amount = graph_utils.find_appropriate_rounding_amount(
            np.concatenate(graph_data.data), allow_scientific=True)

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["yAxis"] = hc_data.convert_axis(graph_data.yAxis)
        new_data["colorAxis"] = {"min": 0, "minColor": "#FFFFFF", "maxColor": "#01c5dd"}

        new_data["yAxis"]["startOnTick"] = False
        new_data["yAxis"]["endOnTick"] = False

        # Fetch data
        data = graph_data.data
        highcharts_data = to_highcharts_matrix(data)
        new_data_regular = []
        for data_point in highcharts_data:
            x = int(data_point[0])
            y = int(data_point[1])
            regular_point = {
                "x": x,
                "y": y,
                "value": data_point[2],
                "x_cat": new_data["xAxis"]["categories"][x],
                "y_cat": new_data["yAxis"]["categories"][y],
            }
            if additional_info is not None:
                regular_point.update(additional_info[y][x])
            new_data_regular.append(regular_point)
        new_data["series"] = [
            {
                "name": "data",
                "borderWidth": graph_data.borderWidth,
                "data": new_data_regular,
                "dataLabels": {
                    "enabled": graph_data.dataLabels,
                    "format": "{point.value:.2f}",
                },
            }
        ]

        # Construct tooltip info
        heatmap_tooltip_dict = graph_data.tooltipKeyDict
        if heatmap_tooltip_dict is None:
            heatmap_tooltip_dict = {
                graph_data.matrixLabel or "Count": graph_utils.round_formatting(
                    "point.value", round_amount
                )
            }

        heatmap_tooltip_format = graph_data.tooltipFormat or \
                                 tooltip.create_tooltip_formatting(
                                     heatmap_tooltip_dict, tooltip_as_table
                                 )
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        new_data["plotOptions"] = {
            "heatmap": {
                "tooltip": {"headerFormat": "", "pointFormat": heatmap_tooltip_format}
            }
        }

        return new_data


HighchartsConverterFactory.register(GraphType.heatMap, HeatMapConverter)