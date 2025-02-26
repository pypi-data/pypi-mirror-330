from typing import Dict, Optional


def create_table_tooltip_formatting(key_value_dict: Dict[str, str], title: Optional[str] = None):
    res = []
    # table_styling = 'border=1 cellpadding=5'
    table_styling = 'style="border:1px solid"'
    cell_key_styling = 'style="border:1px solid; padding:5px"'
    cell_value_styling = 'style="border:1px solid; padding:5px; text-align: right"'
    for k, v in key_value_dict.items():
        key_tooltip = f"<td {cell_key_styling}>{k}</td>"
        value_tooltip = f'<td {cell_value_styling}><b>{v}</b></td>'
        res.append(f"<tr>" + key_tooltip + value_tooltip + "</tr>")
    tooltip_format = f"<table {table_styling}>" + "".join(res) + "</table>"
    if title is not None:
        tooltip_format = "<div style='margin-bottom:5px;text-align:center;'>{}</div>".format(title) + tooltip_format
    return tooltip_format


def create_regular_tooltip_formatting(key_value_dict):
    res = []
    for k, v in key_value_dict.items():
        key_tooltip = "{}: ".format(k)
        value_tooltip = "<b>{}</b>".format(v)
        res.append(key_tooltip + value_tooltip)
    return "<br>".join(res)


def create_tooltip_formatting(key_value_dict: dict, tooltip_as_table: bool = False):
    if tooltip_as_table:
        return create_table_tooltip_formatting(key_value_dict)
    else:
        return create_regular_tooltip_formatting(key_value_dict)
