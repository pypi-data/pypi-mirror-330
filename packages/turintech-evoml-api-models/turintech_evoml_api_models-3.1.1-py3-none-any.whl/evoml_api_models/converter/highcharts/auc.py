import numpy as np

from ... import graphs
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


def convert_auc(graph_data: graphs.AUCCurve):
    # Declare constants
    tooltip_as_table = True

    # Initiate new json
    new_data = dict({"chart": {"type": "areaspline"}})

    # Basic additions to new json
    new_data = hc_data.common_graph_processing(graph_data, new_data)

    # Set axes
    default_xaxis_format = {
        "tickInterval": 0.2,
        "gridLineWidth": 0,
        "min": 0,
        "max": 1,
    }
    default_yaxis_format = {
        "tickInterval": 0.2,
        "min": 0,
        "max": 1.01,
        "endOnTick": False
    }
    given_x_axis = graph_utils.remove_none_values(hc_data.convert_axis(graph_data.xAxis))
    given_y_axis = graph_utils.remove_none_values(hc_data.convert_axis(graph_data.yAxis))
    new_data["xAxis"] = graph_utils.dict_update(default_xaxis_format, given_x_axis)
    new_data["yAxis"] = graph_utils.dict_update(default_yaxis_format, given_y_axis)

    new_data["series"] = []
    for param in graph_data.data:
        new_param_data = []
        additional_info = param.additionalInfo
        thresholds = param.thresholds
        optimal_thresholds = param.optimalThresholds
        for i, point in enumerate(param.data):
            point_data = {
                "x": point[0],
                "y": point[1]
            }
            if thresholds is not None:
                point_data["threshold"] = "N/A" if thresholds[i] > 1 else thresholds[i]
            if additional_info is not None:
                point_data.update(additional_info[i])
            new_param_data.append(point_data)
        if optimal_thresholds is not None:
            for threshold in optimal_thresholds:
                t_index = threshold.index
                new_param_data[t_index]["marker"] = {
                    "enabled": True,
                    "symbol": "circle",
                    "radius": 5.5,
                    "lineWidth": 1.5,
                    "fillColor": "#FFFFFF",
                }
        new_param = {
            "name": "{0} (AUC: {1:.2f})".format(
                graph_utils.html_to_plaintext(param.name), param.aucScore
            ),
            "data": new_param_data,
            "AUC": param.aucScore,
            "className": graph_utils.html_to_plaintext(param.name)
        }
        new_data["series"].append(new_param)

    if graph_data.maxVisible is not None:
        for i in range(graph_data.maxVisible, len(new_data["series"])):
            new_data["series"][i]["visible"] = False

    baselines = graph_data.baselines
    if baselines is not None:
        baselines = [baseline.dict() for baseline in baselines]
        for baseline in baselines:
            baseline["enableMouseTracking"] = False

        new_data["series"].extend([graph_utils.remove_none_values(d) for d in baselines])

    # Construct tooltip info
    default_tooltip_dict = {
        f"{new_data['yAxis']['title']['text']}": "{point.y:.2f}",
        f"{new_data['xAxis']['title']['text']}": "{point.x:.2f}",
    }

    tooltip_dict = graph_data.tooltipKeyDict or default_tooltip_dict
    tooltip_format = graph_data.tooltipFormat or \
                     tooltip.create_tooltip_formatting(
                         tooltip_dict, tooltip_as_table
                     )
    if tooltip_as_table:
        new_data["tooltip"] = {"useHTML": True}

    # Set plot options
    new_data["plotOptions"] = {
        "series": {
            "fillOpacity": 0.1,
            "marker": {"enabled": False, "symbol": "circle", "lineColor": None},
            "tooltip": {"headerFormat": "", "pointFormat": tooltip_format},
        }
    }

    return new_data


class AUCConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.AUCCurve) -> dict:
        return convert_auc(graph_data)


class ROCConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.MultiClassROCCurve):
        graph_dict = graph_data.dict()
        graph_dict['xAxis'] = {'title': 'False Positive Rate'}
        graph_dict['yAxis'] = {'title': 'True Positive Rate', "endOnTick": False}
        if graph_data.showBaselines:
            perfect_classifier_data = [[0, i / 10] for i in range(0, 11)] + [
                [i / 10, 1] for i in range(0, 11)
            ]
            random_classifier_data = [[i / 10, i / 10] for i in range(0, 11)]
            graph_dict['baselines'] = [{
                "name": "Perfect Classifier",
                "type": "spline",
                "zIndex": -1,
                "data": perfect_classifier_data,
                "dashStyle": "ShortDash",
                "color": "#34bfa3"
            }, {
                "name": "Random Classifier",
                "type": "spline",
                "zIndex": -2,
                "data": random_classifier_data,
                "dashStyle": "ShortDash",
                "color": "#FF4136"
            }]

        return convert_auc(graphs.AUCCurve(**graph_dict))


class PRCurveConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.MultiClassPrecisionRecallCurve):
        graph_dict = graph_data.dict()
        graph_dict['xAxis'] = {'title': 'Recall'}
        graph_dict['yAxis'] = {'title': 'Precision', 'endOnTick': False}
        if graph_data.showBaselines:
            baseline_precision = max(
                [param.get("labelProportion") for param in graph_dict["data"]]
            )
            perfect_classifier_data = [[0, 1], [1, 1]]
            random_classifier_data = [[0, baseline_precision], [1, baseline_precision]]
            graph_dict['baselines'] = [{
                "name": "Perfect Classifier",
                "type": "spline",
                "zIndex": -1,
                "data": perfect_classifier_data,
                "dashStyle": "ShortDash",
                "color": "#34bfa3"
            }, {
                "name": "Random Classifier",
                "type": "spline",
                "zIndex": -2,
                "data": random_classifier_data,
                "dashStyle": "ShortDash",
                "color": "#FF4136"
            }]
        return convert_auc(graphs.AUCCurve(**graph_dict))


HighchartsConverterFactory.register(GraphType.aucCurve, AUCConverter)
HighchartsConverterFactory.register(GraphType.rocCurve, ROCConverter)
HighchartsConverterFactory.register(GraphType.precisionRecallCurve, PRCurveConverter)