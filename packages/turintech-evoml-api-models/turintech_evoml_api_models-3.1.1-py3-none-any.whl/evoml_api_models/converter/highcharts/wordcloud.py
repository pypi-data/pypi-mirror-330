import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class WordCloudConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.WordCloud) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Initiate new json
        new_data = dict({"chart": {"type": "wordcloud"}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Fetch data
        new_data["series"] = [{"name": "Count", "data": [point.dict() for point in graph_data.data]}]

        # Construct tooltip info
        wordcloud_tooltip_dict = {"Word": "{point.name}", "Count": "{point.weight:.0f}"}
        if tooltip_as_table:
            wordcloud_tooltip_format = tooltip.create_table_tooltip_formatting(
                wordcloud_tooltip_dict
            )
            new_data["tooltip"] = {"useHTML": True}
        else:
            wordcloud_tooltip_format = tooltip.create_regular_tooltip_formatting(
                wordcloud_tooltip_dict
            )

        # Set plot options
        new_data["plotOptions"] = {
            "wordcloud": {
                "maxFontSize": 55,
                "minFontSize": 15,
                "tooltip": {
                    "headerFormat": "",
                    "pointFormat": wordcloud_tooltip_format,
                }
            }
        }

        return new_data


HighchartsConverterFactory.register(GraphType.wordCloud, WordCloudConverter)