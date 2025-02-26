import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip, error_bar


from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class BarChartConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.BarChart) -> dict:
        # Declare constants
        tooltip_as_table = True

        # Fetch constants from graphJson
        show_gridlines = graph_data.showGridLines
        to_percent = graph_data.dataToPercent

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

        if isinstance(graph_data.yAxis, list):
            new_data["yAxis"] = hc_data.convert_multiple_axis(
                graph_data.yAxis,
                show_labels=False,
                show_gridlines=show_gridlines,
                padding=0.1,
            )
            new_data["xAxis"]["lineWidth"] = 2
            new_data["xAxis"]["lineColor"] = "#000000"
        else:
            new_data["yAxis"] = [
                hc_data.convert_axis(
                    graph_data.yAxis,
                    show_labels=graph_data.type == "column",
                    show_gridlines=show_gridlines,
                    padding=0.1,
                )
            ]

        # Fetch data
        new_data["series"] = [
            hc_data.convert_bar_data(
                series,
                to_percent=to_percent,
                labels=new_data["xAxis"]["categories"],
            )
            for series in graph_data.data
        ]

        # Set visible to maxVisible if it exists
        if graph_data.maxVisible is not None:
            for i in range(graph_data.maxVisible, len(new_data["series"])):
                new_data["series"][i]["visible"] = False

        # Construct tooltip info
        if graph_data.tooltipKeyDict is not None:
            bar_tooltip_dict = graph_data.tooltipKeyDict
        elif to_percent:
            bar_tooltip_dict = {
                "Feature": "{point.x_cat}",
                "{series.name}": "{point.y:.2f}%",
            }
        else:
            bar_tooltip_dict = {
                "Feature": "{point.x_cat}",
                "{series.name}": graph_utils.round_formatting("point.y", round_amount),
            }
            if graph_data.stacking is not None:
                bar_tooltip_dict.update({"Percentage": "{point.percentage:.3f}%"})

        bar_tooltip_format = graph_data.tooltipFormat or \
                             tooltip.create_tooltip_formatting(bar_tooltip_dict, tooltip_as_table)
        if tooltip_as_table:
            new_data["tooltip"] = {"useHTML": True}

        # Set datalabel format
        datalabel_format = graph_utils.round_formatting("point.y", round_amount)

        # If only one element in legend, disable legend
        if len(new_data["series"]) == 1:
            new_data["legend"]["enabled"] = False

        # Set plot options
        new_data["plotOptions"] = {
            "bar": {
                "minPointLength": 2,
                "tooltip": {
                    "headerFormat": "",
                    "pointFormat": bar_tooltip_format,
                },
                "stacking": graph_data.stacking,
            }
        }

        if graph_data.stacking is None:
            new_data["plotOptions"]["bar"].update(
                {
                    "dataLabels": {
                        "enabled": True,
                        "style": {"fontSize": "14px"},
                        "allowOverlap": True,
                        "format": datalabel_format
                    }
                }
            )
        elif graph_data.stacking == "normal":
            for axis in new_data["yAxis"]:
                axis.update(
                    {
                        "stackLabels": {
                            "enabled": True,
                            "align": "right",
                            "style": {"fontSize": "8px"},
                            "format": "{total:.3f}",
                        }
                    }
                )

        if graph_data.errorBarData is not None:
            new_data = error_bar.add_error_bar(graph_data, new_data, to_percent=to_percent)

        if to_percent:
            new_plot_options = {"bar": {"dataLabels": {"format": "{point.y:.1f}%"}}}
            new_data["plotOptions"] = graph_utils.dict_update(new_data["plotOptions"], new_plot_options)

        return new_data


HighchartsConverterFactory.register(GraphType.barChart, BarChartConverter)