import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip, error_bar

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class TimelineConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.TimelineReport) -> dict:
        timeline_dict = dict({"chart": {"type": "timeline"}})

        timeline_dict["xAxis"] = {"visible": False}
        timeline_dict["yAxis"] = {"visible": False}
        timeline_dict["title"] = {"text": "Preprocessing Timeline"}
        timeline_dict["tooltip"] = {"useHTML": True}
        timeline_dict["subtitle"] = {
            "text": "Total time to preprocess data - {} seconds".format(
                graph_data.duration
            )
        }
        data = graph_data.data
        timeline_data = []
        for summary in data:
            step_data = {}
            step_data["name"] = summary.name
            step_data["label"] = summary.description

            # Generate the HTML string for the list of bullet points
            html_description_string = "<ul type='square'>"
            informations = summary.information
            for information in informations:
                html_description_string = (
                    html_description_string
                    + "<li>"
                    + information.replace("'", "")
                    + "</li>"
                )
            html_description_string = html_description_string + "</ul>"
            step_data["description"] = html_description_string
            timeline_data.append(step_data)
        timeline_dict["series"] = [
            {
                "data": timeline_data,
                "dataLabels": {"connectorColor": "orange", "connectorWidth": 2},
            }
        ]
        return timeline_dict


HighchartsConverterFactory.register(GraphType.timelineReport, TimelineConverter)