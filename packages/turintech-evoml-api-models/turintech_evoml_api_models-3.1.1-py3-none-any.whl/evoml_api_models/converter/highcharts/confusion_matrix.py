import numpy as np

from ... import graphs
from ...utils import to_highcharts_matrix
from . import data as hc_data
from . import utils as graph_utils
from . import tooltip

from ...graphs import GraphType
from .interface import HighchartsConverter, HighchartsConverterFactory


class ConfusionMatrixConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.ConfusionMatrix) -> dict:
        # Declare constants
        tooltip_as_table = True
        total_error_label_color = "gray"

        # Fetch constants from graphJson
        show_labels = True if len(graph_data.classLabels) <= 12 else False
        shrink_labels = True if len(graph_data.classLabels) >= 8 else False
        font_size = "8px" if len(graph_data.classLabels) <= 10 else "6px"
        class_labels = [graph_utils.html_to_plaintext(label) for label in graph_data.classLabels]
        x_class_labels = [f"Predicted<br><b>{category}</b>" for category in class_labels]
        y_class_labels = [f"Actual <b>{category}</b>" for category in class_labels]
        x_class_labels_with_extra = np.append(
            x_class_labels, ["<b>Total</b>", "<b>Misclassified</b>"]
        ).tolist()
        y_class_labels_with_extra = np.append(
            y_class_labels, ["<b>Total</b>", "<b>Misclassified</b>"]
        ).tolist()

        # Initiate new json
        new_data = dict({"chart": {"type": "heatmap"}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        # Set axes
        new_data["xAxis"] = {
            "title": {"text": ""},
            "categories": x_class_labels_with_extra,
            "opposite": True,
            "gridLineColor": "#808080",
            "gridLineWidth": 1,
            "lineColor": "#808080",
            "labels": {"step": 1, "align": "center"},
        }
        new_data["yAxis"] = {
            "title": {"text": ""},
            "categories": y_class_labels_with_extra,
            "reversed": True,
            "gridLineColor": "#808080",
            "gridLineWidth": 1,
            "labels": {"step": 1, "align": "center"},
        }

        if shrink_labels:
            new_data["xAxis"]["labels"].update({"style": {"fontSize": font_size}})
            new_data["yAxis"]["labels"].update({"style": {"fontSize": font_size}})
            label_style = {"fontSize": font_size, "textOutline": None}
        else:
            label_style = {"textOutline": None}

        # Fetch data
        # First, fetch regular points of confusion matrix
        new_data_regular = []
        new_data_normalized = []
        data = graph_data.data
        highcharts_data = to_highcharts_matrix(data)
        data_matrix = np.zeros((len(class_labels), len(class_labels)))
        full_total = np.sum([i[2] for i in highcharts_data])
        for data_point in highcharts_data:
            column_sum = sum([i[2] for i in highcharts_data if i[0] == data_point[0]])
            row_sum = sum([i[2] for i in highcharts_data if i[1] == data_point[1]])
            x_cat = class_labels[int(data_point[0])]
            y_cat = class_labels[int(data_point[1])]
            percentage_predicted = 0 if column_sum == 0 else (100 * data_point[2] / column_sum)
            percentage_actual = 0 if row_sum == 0 else (100 * data_point[2] / row_sum)
            percentage_total = 0 if full_total == 0 else (100 * data_point[2] / full_total)
            regular_point = {
                "x": data_point[0],
                "y": data_point[1],
                "x_cat": x_cat,
                "y_cat": y_cat,
                "value": data_point[2] if x_cat == y_cat else -data_point[2],
                "classification_status": "Correctly Classified" if x_cat == y_cat else "Misclassified",
                "count": data_point[2],
                "percentage": percentage_total,
                "row1_label": f"Percentage of Predicted <b>{x_cat}</b>",
                "row2_label": f"Percentage of Actual <b>{y_cat}</b>",
                "row1_value": f"{percentage_predicted:.0f}%",
                "row2_value": f"{percentage_actual:.0f}%",
            }
            new_data_regular.append(regular_point)
            normalized_point = {"unit": "%"}
            normalized_point.update(regular_point)
            new_data_normalized.append(normalized_point)
            data_matrix[int(data_point[0])][int(data_point[1])] = data_point[2]

        # Fetch Total/Error sections of confusion matrix
        number_categories_total = len(x_class_labels_with_extra)
        total_over_x = np.sum(data_matrix, axis=0)
        total_over_y = np.sum(data_matrix, axis=1)
        error_count_over_x = total_over_x - np.diag(data_matrix)
        error_count_over_y = total_over_y - np.diag(data_matrix)
        error_count_total = np.sum(error_count_over_x)
        error_percent_over_x = error_count_over_x / np.where(
            total_over_x == 0, 1e-8, total_over_x
        )
        error_percent_over_y = error_count_over_y / np.where(
            total_over_y == 0, 1e-8, total_over_y
        )
        for i in range(0, number_categories_total - 2):
            precision = 100 * (1 - error_percent_over_y[i])
            recall = 100 * (1 - error_percent_over_x[i])
            percentage_total = 100 if full_total == 0 else 100*total_over_y[i]/full_total
            category = class_labels[i]
            y_total_point = {
                "x": i,
                "y": number_categories_total - 2,
                "x_cat": new_data["xAxis"]["categories"][i],
                "y_cat": "Total",
                "value": 0,
                "count": total_over_y[i],
                "percentage": percentage_total,
                "row1_label": f"Number Misclassified (Predicted <b>{category}</b>)",
                "row2_label": f"Precision (<b>{category}</b>)",
                "row1_value": f"{error_count_over_y[i]:.0f}",
                "row2_value": f"{precision:.0f}%",
                "classification_status": f"Total (Predicted <b>{category}</b>)",
                "unit": "%",
                "label_prefix": f'<p style="color:{total_error_label_color};">',
                "label_suffix": "</p>",
            }
            x_total_point = {
                "x": number_categories_total - 2,
                "y": i,
                "x_cat": "Total",
                "y_cat": new_data["yAxis"]["categories"][i],
                "value": 0,
                "count": total_over_x[i],
                "percentage": 100 if full_total == 0 else 100*total_over_x[i]/full_total,
                "row1_label": f"Number Misclassified (Actual <b>{category}</b>)",
                "row2_label": f"Recall (<b>{category}</b>)",
                "row1_value": f"{error_count_over_x[i]:.0f}",
                "row2_value": f"{recall:.0f}%",
                "classification_status": f"Total (Actual <b>{category}</b>)",
                "unit": "%",
                "label_prefix": f'<p style="color:{total_error_label_color};">',
                "label_suffix": "</p>",
            }
            new_data_regular.extend(
                [x_total_point, y_total_point]
            )
            new_data_normalized.extend(
                [x_total_point, y_total_point]
            )

        # Set bottom right square of confusion matrix
        accuracy = 100 if full_total == 0 else 100 * (1 - error_count_total/full_total)
        full_total_point = {
                "x": number_categories_total - 2,
                "y": number_categories_total - 2,
                "x_cat": "Total",
                "y_cat": "Total",
                "value": 0,
                "count": np.sum(total_over_x).round(0),
                "percentage": 100,
                "row1_label": "Number Misclassified",
                "row2_label": "Accuracy",
                "row1_value": f"{error_count_total:.0f}",
                "row2_value": f"{accuracy:.0f}%",
                "classification_status": "Total",
                "unit": "%",
                "label_prefix": f'<p style="color:{total_error_label_color};">',
                "label_suffix": "</p>",
            }

        for data in [new_data_regular, new_data_normalized]:
            data.append(full_total_point)

        # Set data to series
        new_data["series"] = [
            {
                "name": "Normalized",
                "color": "black",
                "borderWidth": 0.1,
                "data": new_data_normalized,
                "dataLabels": {
                    "enabled": show_labels,
                    "color": "#000000",
                    "format": "{point.label_prefix}{point.percentage:.0f}{point.unit}{point.label_suffix}",
                    "style": label_style,
                },
                "showInLegend": True,
                "opacity": 1,
                "visible": False,
            },
            {
                "name": "Data",
                "borderWidth": 0.1,
                "data": new_data_regular,
                "showInLegend": False,
                "dataLabels": {
                    "enabled": show_labels,
                    "color": "#000000",
                    "format": "{point.label_prefix}{point.count:.0f}{point.label_suffix}",
                    "style": label_style,
                },
            },
        ]

        # Construct tooltip info
        confusion_tooltip_dict = {
            "{point.classification_status}": "{point.count:.0f} ({point.percentage:.0f}%)",
            "{point.row1_label}": "{point.row1_value}",
            "{point.row2_label}": "{point.row2_value}",
        }

        confusion_tooltip_format = tooltip.create_tooltip_formatting(
            confusion_tooltip_dict, tooltip_as_table
        )
        confusion_tooltip_format = (
            "{point.prefix}" + confusion_tooltip_format + "{point.suffix}"
        )

        new_data["tooltip"] = {
            "shared": True,
            "useHTML": True,
            "headerFormat": "",
            "pointFormat": confusion_tooltip_format,
        }

        # Set plot options
        new_data["plotOptions"] = {"series": {"states": {"inactive": {"opacity": 1}, "hover": None}}}

        new_data["colorAxis"] = {
            "stops": [[0, "#FF4136"], [0.5, "#FFFFFF"], [1, "#34bfa3"]],
            "min": -np.max(data_matrix),
            "max": np.max(data_matrix),
            "showInLegend": False
        }

        return new_data


HighchartsConverterFactory.register(GraphType.confusionMatrix, ConfusionMatrixConverter)