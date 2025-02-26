import datetime
import itertools

from ... import graphs
from . import data as hc_data

from ...graphs import GraphType, CalendarOptions
from .interface import HighchartsConverter, HighchartsConverterFactory

from enum import Enum
from typing import Tuple, Dict, List
import calendar


COLOURS = {
    0: "#1d1145",
    1: "#00c5dc",
    2: "#ff851b",
    3: "#34bfa3",
    4: "#ffdc00",
    5: "#058dc7",
    6: "#50b432",
    7: "#ed561b",
}
# Note: for calendar we have to specify colors manually so that they are the
# same for dates with the same top category as we plot them as separate series
# each (which is done for unique tooltip).


class CalendarPlotConverter(HighchartsConverter):
    def convert_data(self, graph_data: graphs.CalendarPlot) -> dict:
        assert graph_data.calendar_type in CalendarOptions, "Invalid calendar type"

        # Initiate new json
        new_data = dict({"chart": {"type": "heatmap", "height": 500}})

        # Basic additions to new json
        new_data = hc_data.common_graph_processing(graph_data, new_data)

        new_data["xAxis"] = {
            "type": "category",
            "title": None,
            "lineWidth": 0,
            "reversed": False,
            "opposite": True,
            "gridLineWidth": 0,
            "minorGridLineWidth": 1,
            "minTickInterval": 1,
        }

        new_data["yAxis"] = {
            "type": "category",
            "title": None,
            "gridLineWidth": 0,
            "minorGridLineWidth": 0,
            "tickWidth": 0,
            "reversed": True,
            "lineWidth": 0,
        }

        new_data["plotOptions"] = {"series": {"borderColor": "#ffffff", "borderWidth": 3, "stickyTracking": False}}

        new_data["tooltip"] = {"useHTML": True}

        # ─────────────────────── Tooltip construction ───────────────────────
        # Whether we have many categories and need to specify "Top 10" in the
        # tooltip
        top_10 = len(graph_data.categories) > 10

        # This will be used by individual dates 'blocks' when creating tooltips.
        category_keys: List[str] = [
            v for _ in [[f"cat_{i}_name", f"cat_{i}_value"] for i in range(len(graph_data.categories))] for v in _
        ]

        def create_tooltip(categories: List[str], table_width: int = 87) -> str:
            tooltip_dict = {
                f"{{point.{categories[i]}}}": f"{{point.{categories[i + 1]}}}"
                for i in range(0, len(categories), 2)
            }

            res = []

            # 87 pixels is the minimum width of the table by default, 140 px is
            # the minimum when we specify "Top 10" in the title
            table_styling = f'style="border:0px solid; width:{table_width}px"'
            cell_key_styling = 'style="border:0px solid; padding:5px"'
            cell_value_styling = 'style="border:0px solid; padding:5px; text-align: right"'

            for k, v in tooltip_dict.items():
                key_tooltip = f"<td {cell_key_styling}>{k}</td>"
                value_tooltip = f"<td {cell_value_styling}><b>{v}</b></td>"
                res.append(f"<tr>{key_tooltip}{value_tooltip}</tr>")

            return f"<table {table_styling}>" + "".join(res) + "</table>"

        # ┌───────────────────────────────────────────────────────────────────┐
        # │          Case when we are visualising for a single year           │
        # └───────────────────────────────────────────────────────────────────┘
        if graph_data.calendar_type == CalendarOptions.single_year:
            new_data["xAxis"]["categories"] = [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
                "",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
                "",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
                "",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
                "",
            ]
            new_data["yAxis"]["labels"] = {"enabled": False}

            # Colour Axis is used to force colours onto the heatmap
            # In the case of a calendar we need white and gray colour
            # to distinguish actual dates and empty spaces, also to
            # have a white background for letters representing month
            # names.
            new_data["colorAxis"] = {
                "min": 0,
                "max": 10,
                "tickInterval": 1,
                "tickmarkPlacement": "on",
                "stops": [[0, "#ffffff"], [0.1, "#eeeeee"]],  # white and light-gray
                "labels": {"enabled": True},
                "showInLegend": False,
            }

            # ────────────────────── Generating calendar ──────────────────────
            def generate_month_json(name: str, x: int, y: int, start: int, n_days: int) -> Tuple[Dict, bool]:
                """Generates a dictionary with parameters and data to visualise
                a single month on a heat-map.

                Args:
                    name (str):
                        Name of the heat-map dictionary
                    x (int):
                        Origin coordinate (horizontal). This is the upper-left
                        corner block.
                        For example, January is the first month, thus it's
                        origin_x should be 0.
                    y (int):
                        Same as origin_x but vertical
                    start (int):
                        Which day of the week is the first day of the month.
                        This is essentially a horizontal offset.
                    n_days (int):
                        How many days in that month (i.e. how many heat-map
                        blocks to generate)

                Returns:
                    month_series (Dict):
                        Dictionary compatible with Highcharts API for heat-map
                    y_offset (bool):
                        Vertical offset that the month created. This is False
                        for most cases, True iff a month needs 6 rows. That
                        happens when a month starts on a weekend.

                Raises:
                    AssertionError: if n_days is not within 28 to 31 range

                """
                assert 28 <= n_days <= 31, "Invalid number of days"
                first_week_offset = start
                y_offset = 0
                month_data = []
                for day in range(1, n_days + 1):
                    if y_offset == 0:
                        x_pos = x + start + day - 1
                    else:
                        x_pos = x + start + day - ((8 - first_week_offset) + 7 * (y_offset - 1))
                    if x_pos > x + 6:
                        y_offset += 1
                        start = 0
                        x_pos = x + start + day - ((8 - first_week_offset) + 7 * (y_offset - 1))
                    y_pos = y + y_offset
                    month_data.append([x_pos, y_pos, 1, day])

                month_series = {
                    "name": name,
                    "keys": ["x", "y", "value", "day"],
                    "data": month_data,
                    "showInLegend": False,
                    "enableMouseTracking": False,
                    "dataLabels": {
                        "enabled": True,
                        "crop": False,
                        "overflow": "allow",
                        "format": "{point.day}",
                        "style": {"fontSize": "9px", "color": "#999999", "fontWeight": "normal", "textOutline": "none"},
                    },
                }
                return month_series, y_offset > 4

            # Defining constants
            year_to_visualise = graph_data.years_to_visualise[0]
            middle_months_offset, final_months_offset = 0, 0

            # Generating heatmaps
            # First row of months is always located on row 0, but if at least
            # one of the months starts on a weekend it is automatically taking
            # up more space in terms of height. Such cases have to be caught
            # so that other months and their names are not overlapping.
            months = {
                "January": 31,
                "February": 29 if calendar.isleap(year_to_visualise) else 28,
                "March": 31,
                "April": 30,
                "May": 31,
                "June": 30,
                "July": 31,
                "August": 31,
                "September": 30,
                "October": 31,
                "November": 30,
                "December": 31,
            }
            y = [0] * 4 + [6] * 4 + [12] * 4
            offsets = []
            new_data["series"] = []

            for i, (name, day) in enumerate(months.items()):
                month_json, month_offset = generate_month_json(
                    name, (i + 4) % 4 * 8, y[i], calendar.weekday(year_to_visualise, i + 1, 1), day
                )
                new_data["series"].append(month_json)
                offsets.append(month_offset)
                # This block is to manage the offset that can occur when a
                # month has an extra week overflow
                if i in [3, 7] and any(_ > 0 for _ in offsets):
                    if i == 3:
                        middle_months_offset += 1
                        y[4:8] = [6 + middle_months_offset] * 4
                    final_months_offset += 1
                    y[8:12] = [12 + final_months_offset] * 4
                    offsets = []

            # Month names
            # Note: offsets are used so that month names do not overlap with
            # the actual month dates.
            letters = list("JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC")
            x_vals = [j for _ in [[i, i + 1, i + 2] for i in [2, 10, 18, 26]] for j in _] * 3
            y_vals = [-1] * 12 + [5 + middle_months_offset] * 12 + [11 + final_months_offset] * 12
            new_data["series"].append(
                {
                    "name": "Month names",
                    # "value" is set to 0 to make the background white (refer to
                    # colorAxis)
                    "keys": ["x", "y", "value", "letter"],
                    "data": [[x_vals[i], y_vals[i], 0, letters[i]] for i in range(36)],
                    "states": {"hover": {"enabled": False}},
                    "enableMouseTracking": False,
                    "showInLegend": False,
                    "dataLabels": {
                        "enabled": True,
                        "crop": False,
                        "overflow": "allow",
                        "format": "<b>{point.letter}</b>",
                        "style": {
                            "fontSize": "14px",
                            "color": "#999999",
                            "fontWeight": "normal",
                            "textOutline": "none",
                        },
                    },
                }
            )

            # ───────────────────── Populating the calendar ─────────────────────
            def find_coordinates(date: datetime.datetime, mid_offset: int, fin_offset: int) -> Tuple[int, int]:
                # Given datetime find where it is on the heat map
                month, day = date.month, date.day
                if month in [1, 2, 3, 4]:
                    y = 0
                elif month in [5, 6, 7, 8]:
                    y = 6 + mid_offset
                else:
                    y = 12 + fin_offset

                x = (month + 3) % 4 * 8
                x_offset = calendar.weekday(year_to_visualise, month, 1)
                y += (day + x_offset - 1) // 7
                x += (day + x_offset - 1) % 7
                return x, y

            # Keeping track of top categories that we are plotting. This is
            # needed because date blocks that have a top category that was
            # already saved has to be "linkedTo" so that the legend connects
            # them. If not, we need a unique "id" so that future dates of the
            # same top category can be "linkedTo" it. Will also contain info on
            # what colour was used for a category.
            top_cats = {cat: None for cat in graph_data.categories}
            _id = 0

            # Going through each CalendarData object and combining the
            # information to a Highcharts compatible format, creating a
            # separate series for each date so that it has a unique tooltip.
            # Each series will have keys in the following format:
            # [x_position, y_position, unix_datetime, cat_1_name,
            # cat_1_value, ... , cat_n_name, cat_n_value]
            # where cat_1 through cat_n are all the relevant (for that date)
            # categories.
            # We have to keep both name and value for each relevant category
            # so that we can have correct category name and value for the
            # tooltip table.
            for data_point in graph_data.data:
                x, y = find_coordinates(data_point.date, middle_months_offset, final_months_offset)
                unix_dt = data_point.date.timestamp() * 1000
                cat_freq = data_point.cat_frequencies

                # Getting rid of categories that have 0 frequency, keeping top 10 max
                sorted_cat = sorted(zip(cat_freq, graph_data.categories), reverse=True)[:10]
                sorted_cat = [pair for pair in sorted_cat if pair[0] > 0]

                # If all category frequencies turned out 0, we do not
                # visualise for that date and leave it as a grey block
                if not sorted_cat:
                    continue

                sorted_cat_freq = [pair[0] for pair in sorted_cat]
                sorted_cat_names = [pair[1] for pair in sorted_cat]

                # category name and corresponding frequency for all categories
                # alternating, e.g.: "cat_1", 5, "cat_2", 3
                cat_name_freq_alternating = list(
                    itertools.chain.from_iterable(zip(sorted_cat_names, sorted_cat_freq))
                )
                cat_name_freq_str_repr = category_keys[:len(sorted_cat_names) * 2]

                # Category that has the highest occurrence on that date
                top_cat_name = sorted_cat_names[0]

                # Finally, construction of a Highcharts compatible series point
                series_point = {
                    "name": top_cat_name,
                    "keys": ["x", "y", "unix", "cat_num"] + cat_name_freq_str_repr,
                    "data": [[x, y, unix_dt, len(sorted_cat_freq)] + cat_name_freq_alternating],
                    "tooltip": {
                        "headerFormat": "",
                        "pointFormat": f"{f'(Top {{point.cat_num}}) ' if top_10 else ''}"
                                       + "Category counts <br>on <b>{point.unix:%Y-%m-%d}</b>:<br>"
                                       + create_tooltip(cat_name_freq_str_repr, table_width=140 if top_10 else 87)
                    },
                    "legendIndex": graph_data.categories.index(top_cat_name),
                }

                if top_cats[top_cat_name] is None:
                    top_cats[top_cat_name] = (_id, _id % len(COLOURS))
                    series_point["id"] = str(_id)
                    series_point["color"] = COLOURS[_id % len(COLOURS)]
                    _id += 1
                else:
                    series_point["linkedTo"] = str(top_cats[top_cat_name][0])
                    series_point["color"] = COLOURS[top_cats[top_cat_name][1]]

                new_data["series"].append(series_point)

        # ┌───────────────────────────────────────────────────────────────────┐
        # │          Case when we are visualising for 2 to 15 years           │
        # └───────────────────────────────────────────────────────────────────┘
        else:
            new_data["xAxis"]["categories"] = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            new_data["yAxis"]["categories"] = [str(_) for _ in reversed(graph_data.years_to_visualise)]

            # ────────────────────── Generating calendar ──────────────────────
            new_data["series"] = [
                {
                    "name": "Gray blocks",
                    "keys": ["x", "y", "value"],
                    "color": "#eeeeee",
                    "showInLegend": False,
                    "enableMouseTracking": False,
                    "data": [
                        [x, y] for x, y in itertools.product(range(12), range(len(graph_data.years_to_visualise)))
                    ],
                }
            ]

            # ──────────────────── Populating the calendar ────────────────────
            # Keeping track of top categories that we are plotting. This is
            # needed because date blocks that have a top category that was
            # already saved has to be "linkedTo" so that the legend connects
            # them. If not, we need a unique "id" so that future dates of the
            # same top category can be "linkedTo" it. Will also contain info on
            # what colour was used for a category.
            top_cats = {cat: None for cat in graph_data.categories}
            _id = 0

            reversed_years = [i for i in reversed(graph_data.years_to_visualise)]

            # Going through each CalendarData object and combining the
            # information to a Highcharts compatible format, creating a
            # separate series for each date so that it has a unique tooltip.
            # Each series will have keys in the following format:
            # [x_position, y_position, unix_datetime, cat_1_name,
            # cat_1_value, ... , cat_n_name, cat_n_value]
            # where cat_1 through cat_n are all the relevant (for that date)
            # categories.
            # We have to keep both name and value for each relevant category
            # so that we can have correct category name and value for the
            # tooltip table.
            for data_point in graph_data.data:
                # Making sure there are categories that appeared on that date
                if sum(data_point.cat_frequencies) == 0:
                    continue

                x = data_point.date.month - 1
                y = reversed_years.index(data_point.date.year)
                unix_dt = data_point.date.timestamp() * 1000
                cat_freq = data_point.cat_frequencies

                # Getting rid of categories that have 0 frequency, keeping top 10 max
                sorted_cat = sorted(zip(cat_freq, graph_data.categories), reverse=True)[:10]
                sorted_cat = [pair for pair in sorted_cat if pair[0] > 0]
                sorted_cat_freq = [pair[0] for pair in sorted_cat]
                sorted_cat_names = [pair[1] for pair in sorted_cat]

                # category name and corresponding frequency for all categories
                # alternating, e.g.: "cat_1", 5, "cat_2", 3
                cat_name_freq_alternating = [
                    v
                    for _ in [[i, j] for i, j in zip(sorted_cat_names, sorted_cat_freq)]
                    for v in _
                ]

                cat_name_freq_str_repr = category_keys[:len(sorted_cat_names) * 2]

                # Category that has the highest occurrence on that date
                top_cat_name = sorted_cat_names[0]

                # Finally, construction of a Highcharts compatible series point
                series_point = {
                    "name": top_cat_name,
                    "keys": ["x", "y", "unix", "count", "cat_num"] + cat_name_freq_str_repr,
                    "data": [[x, y, unix_dt, max(cat_freq), len(sorted_cat_freq)] + cat_name_freq_alternating],
                    "tooltip": {
                        "headerFormat": "",
                        "pointFormat": f"{f'(Top {{point.cat_num}}) ' if top_10 else ''}"
                                       + "Category counts <br>on <b>{point.unix:%Y-%m}</b>:<br>"
                                       + create_tooltip(cat_name_freq_str_repr, table_width=140 if top_10 else 87),
                    },
                    "legendIndex": graph_data.categories.index(top_cat_name),
                    "dataLabels": {
                        "enabled": True,
                        "crop": False,
                        "overflow": "allow",
                        "format": "<b>{point.count}</b>",
                        "style": {"fontSize": "12px", "fontWeight": "normal", "textOutline": "none"},
                    },
                }

                if top_cats[top_cat_name] is None:
                    top_cats[top_cat_name] = (_id, _id % len(COLOURS))
                    series_point["id"] = str(_id)
                    series_point["color"] = COLOURS[_id % len(COLOURS)]
                    _id += 1
                else:
                    series_point["linkedTo"] = str(top_cats[top_cat_name][0])
                    series_point["color"] = COLOURS[top_cats[top_cat_name][1]]

                new_data["series"].append(series_point)

        return new_data


HighchartsConverterFactory.register(GraphType.calendarPlot, CalendarPlotConverter)
