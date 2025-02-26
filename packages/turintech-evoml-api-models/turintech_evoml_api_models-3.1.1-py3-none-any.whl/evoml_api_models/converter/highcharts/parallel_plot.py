import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class ParallelPlotConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.ParallelPlot) -> dict:

        new_data = dict(
            {
                "chart": {
                    "type": "spline",
                    "parallelCoordinates": True,
                    "parallelAxes": {"lineWidth": 2}
                },
                "title": graph_data.title
            }
        )

        # Setting up Axes
        new_data["xAxis"] = graph_data.xAxis
        new_data["yAxis"] = graph_data.yAxis

        new_data["legend"] = {"enabled": True}

        # Data to plot
        new_data["series"] = []

        first_non_anom = next(iter(graph_data.inliers.items()))
        new_data["series"].append({
            "name": "Inliers",
            "color": "blue",
            "id": str(first_non_anom[0]),
            "data": first_non_anom[1]
        })
        for row_id, row_data in graph_data.inliers.items():
            if first_non_anom[0] == row_id:
                continue
            new_data["series"].append({
                "name": "Inliers",
                "color": "blue",
                "id": str(row_id),
                "linkedTo": str(first_non_anom[0]),
                "data": row_data
            })

        first_anom = next(iter(graph_data.outliers.items()))
        new_data["series"].append({
            "name": "Outliers",
            "color": "red",
            "id": str(first_anom[0]),
            "data": first_anom[1]
        })
        for row_id, row_data in graph_data.outliers.items():
            if first_anom[0] == row_id:
                continue
            new_data["series"].append({
                "name": "Outliers",
                "color": "red",
                "id": str(row_id),
                "linkedTo": str(first_anom[0]),
                "data": row_data
            })

        new_data["plotOptions"] = {
            "spline": {
                "marker": {"symbol": "circle", "enabled": False},
                "tooltip": {
                    "headerFormat": f"<b>Row index: {{series.options.id}}</b><br>",
                    "pointFormat": f"{{point.formattedValue}}"
                }
            }
        }

        return new_data


HighchartsConverterFactory.register(GraphType.parallelPlot, ParallelPlotConverter)
