import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class WaterfallConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.Waterfall) -> dict:
        # Declare tooltip formatting depending on point
        y_axis_name = graph_data.yAxis.title or "y"
        tooltip_point_dict = {
            "start": "Value of " + y_axis_name + " at {point.name} is {point.total}",
            "increase": "{point.name} increases " + y_axis_name + " by {point.y_abs}",
            "decrease": "{point.name} decreases " + y_axis_name + " by {point.y_abs}",
            "unchanged": "{point.name} does not change " + y_axis_name,
            "sum": "Value of " + y_axis_name + " at {point.name} is {point.total}",
            "intermediateSum": "Value of " + y_axis_name + " at {point.name} is {point.total}",
        }
        if graph_data.tooltip is not None:
            for k, v in graph_data.tooltip.dict().items():
                if v is not None:
                    tooltip_point_dict.update({k: v})

        # Replace point attribute access with dictionary access
        for key in tooltip_point_dict:
            tooltip = tooltip_point_dict[key]
            for point_key in ["name", "y", "y_abs", "total"]:
                tooltip = tooltip.replace(
                    "{" + f"point.{point_key}" + "}", "{point" + f"[{point_key}]" + "}"
                )
            tooltip_point_dict[key] = tooltip

        waterfall_points = []
        total = 0
        for data in graph_data.data:
            total += data.y or 0
            sign = "+" if total > 0 else ""
            if data.isStart:
                point = {
                    "name": data.name,
                    "y": data.y,
                    "color": "#D3D3D3",
                    "total": total,
                    "labelText": f"{total}"
                }
                point["tooltipText"] = tooltip_point_dict["start"].format(point=point)
                waterfall_points.append(point)
            elif data.isSum:
                point = {
                    "name": data.name,
                    "isSum": True,
                    "color": "#484452",
                    "total": total,
                    "labelText": f"{total}"
                }
                point["tooltipText"] = tooltip_point_dict["sum"].format(point=point)
                waterfall_points.append(point)
            elif data.isIntermediateSum:
                point = {
                    "name": data.name,
                    "isIntermediateSum": True,
                    "color": "#D3D3D3",
                    "total": total,
                    "labelText": f"{total}"
                }
                point["tooltipText"] = tooltip_point_dict["intermediateSum"].format(point=point)
                waterfall_points.append(point)
            else:
                point = {"name": data.name, "y": data.y, "y_abs": abs(data.y)}
                if point["y"] > 0:
                    point["labelText"] = f"+{point['y']}"
                    point["tooltipText"] = tooltip_point_dict["increase"].format(
                        point=point
                    )
                elif point["y"] < 0:
                    point["labelText"] = f"{point['y']}"
                    point["tooltipText"] = tooltip_point_dict["decrease"].format(
                        point=point
                    )
                else:
                    point["labelText"] = ""
                    point["tooltipText"] = tooltip_point_dict["unchanged"].format(
                        point=point
                    )
                waterfall_points.append(point)

        new_series = {
            "upColor": "#201444",#"#00FF00",
            "color": "red",
            "data": waterfall_points,
            "dataLabels": {"enabled": True, "format": "{point.labelText}"},
        }

        new_data = dict({"chart": {"type": "waterfall", "inverted": True}})
        chart_size = graph_data.chartSize
        if chart_size is not None:
            new_data["chart"]["height"] = chart_size[0]
            new_data["chart"]["width"] = chart_size[1]

        new_data["xAxis"] = hc_data.convert_axis(graph_data.xAxis)
        new_data["xAxis"]["type"] = "category"
        new_data["yAxis"] = hc_data.convert_axis(graph_data.yAxis)
        new_data["yAxis"]["plotLines"] = [{
                "color": "black",
                "dashStyle": "dot",
                "width": 1,
                "value": 0,
                "zIndex": len(new_series) + 1
            }]
        new_data["series"] = [new_series]
        new_data["legend"] = {"enabled": False}
        new_data["plotOptions"] = {
            "waterfall": {
                "dashStyle": "shortDash",
                "tooltip": {"headerFormat": "", "pointFormat": "{point.tooltipText}"},
            }
        }

        return new_data


HighchartsConverterFactory.register(GraphType.Waterfall, WaterfallConverter)