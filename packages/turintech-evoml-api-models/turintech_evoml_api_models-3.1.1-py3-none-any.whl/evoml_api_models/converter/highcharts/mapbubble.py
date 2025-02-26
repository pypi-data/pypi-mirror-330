from ... import graphs
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class GeoLocationConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.GeoLocationPlot) -> dict:
        new_data = {"topology": graph_data.map_link,
                    "title": {"text": graph_data.title}}

        # Actual map (GeoJSON)
        new_data["series"] = [{
            "showInLegend": False,
            "name": "Basemap",
            "color": "#606060",
            "enableMouseTracking": True
        }]

        new_data["series"].append({
            "type": "mapbubble",
            "tooltip": {"pointFormat": "{point.z:.0f}"},
            "dataLabels": {
                "enabled": True,
                "format": "{point.z}"
            },
            "name": graph_data.name_label,
            "joinBy": [
                "hc-key"
            ],
            "visible": False if graph_data.data.map_points else True,
            "data": [{"hc-key": i.hc_key, "z": i.z} for i in graph_data.data.map_bubbles]
        })

        tooltip_format = tooltip.create_tooltip_formatting(
            {i: f"{{point.{j}}}" for i, j in zip(["Latitude", "Longitude"], ["lat", "lon"])}
        )

        if graph_data.data.map_points:
            new_data["series"].append({
                "type": "mappoint",
                "tooltip": {
                    "headerFormat": "",
                    "pointFormat": tooltip_format
                },
                "dataLabels": {"enabled": False},
                "name": "Latitude Longitude scatter",
                "data": [{"lat": i.lat, "lon": i.lon} for i in graph_data.data.map_points]
            })

        return new_data


HighchartsConverterFactory.register(GraphType.geolocationPlot, GeoLocationConverter)