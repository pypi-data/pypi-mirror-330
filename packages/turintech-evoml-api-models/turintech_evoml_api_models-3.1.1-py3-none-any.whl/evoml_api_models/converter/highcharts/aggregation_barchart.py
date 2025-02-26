import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class AggregationBarChartConverter(HighchartsConverter):

    def convert_data(self, graph_data: graphs.BarChart) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Fetch constants from graphJson
        show_gridlines = graph_data.showGridLines

        # Initiate new json
        new_data = dict({"chart": {"type": graph_data.type}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch rounding amount
        all_data = np.concatenate([series.data for series in graph_data.data])
        round_amount = graph_utils.find_appropriate_rounding_amount(all_data, allow_scientific=True)

        # Set axes
        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["xAxis"]["categories"] = [
            graph_utils.html_to_plaintext(label) for label in graph_data.labels
        ]
        new_data["yAxis"] = hc_data.convert_axis(
            graph_data.yAxis, show_gridlines=show_gridlines
        )

        # Fetch data
        new_data["series"] = [
            hc_data.convert_bar_data(series, labels=new_data["xAxis"]["categories"])
            for series in graph_data.data
        ]

        for i, data in enumerate(new_data["series"]):
            data["name"] = graph_utils.html_to_plaintext(str(data["name"])).capitalize()
            if i >= 1:
                data["visible"] = False

        # Construct tooltip info
        agg_tooltip_dict = graph_data.tooltipKeyDict
        if agg_tooltip_dict is None:
            agg_tooltip_dict = {
                f"{graph_data.xAxis.title or 'Label'}": "{point.x_cat}",
                "{series.name}": graph_utils.round_formatting("point.y", round_amount),
            }

        agg_tooltip_format = graph_data.tooltipFormat or \
                             tooltip.create_tooltip_formatting(agg_tooltip_dict, tooltip_as_table)
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        new_data["plotOptions"] = {
            "bar": {
                "minPointLength": 1,
                "negativeColor": "red",
                "threshold": 0,
                "tooltip": {"headerFormat": "", "pointFormat": agg_tooltip_format},
            }
        }

        return new_data


HighchartsConverterFactory.register(GraphType.aggregationBarChart, AggregationBarChartConverter)