import gw_ui_streamlit._create_ui as _create_ui

"""Exposes some of the private _create_ui functions"""
def build_columns(item):
    columns = _create_ui.build_columns(item)
    return columns

def build_dataframe(item, columns, default_rows):
    df = _create_ui.build_dataframe(item, columns, default_rows)
    return df