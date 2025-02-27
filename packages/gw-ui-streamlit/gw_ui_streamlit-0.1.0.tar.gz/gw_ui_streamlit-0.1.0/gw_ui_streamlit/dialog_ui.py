import math

import gw_ui_streamlit.core as gws
import gw_ui_streamlit._create_ui as create_ui
from gw_ui_streamlit.utils import construct_function


@gws.st.dialog(title="Add Row", width="large")
def table_row_add_dialog(table_input, dialog_values={}):
    if "dialog_inputs" not in gws.st.session_state:
        dialog_inputs = []
    else:
        dialog_inputs = gws.st.session_state["dialog_inputs"]
    if dialog_values is None:
        return
    #
    # Set the Dialog Anchor to the first column if it is not set
    #
    if table_input.DialogAnchor is not None:
        column = next(
            itemm for itemm in table_input.Columns if itemm.Code == table_input.DialogAnchor
        )
        create_ui.build_input(gws, column, dialog_values, dialog="Add")
        process_dialog_inputs(table_input)
    #
    # Construct the placeholders for the rest of the inputs
    #
    placeholder = gws.st.empty()
    container = placeholder.container(border=True)
    #
    # Generate the rest of the inputs in the container
    #
    for column in table_input.Columns:
        if table_input.DialogInputs is not None:
            if dialog_inputs == "all" or column.Code in dialog_inputs:
                if column.Code != table_input.DialogAnchor:
                    create_ui.build_input(
                        gws, column, dialog_values, dialog="Add", location=container
                    )
        else:
            if column.Code != table_input.DialogAnchor:
                create_ui.build_input(
                    gws, column, dialog_values, dialog="Add", location=container
                )
    #
    # Add the submit button to the botom of the dialog
    #
    if gws.st.button("Submit"):
        update_df(table_input, dialog_values)
        gws.st.rerun()


@gws.st.dialog(title="Edit Row", width="large")
def table_row_edit_dialog(table_input, row, selected_index, dialog_values):
    if dialog_values is None:
        gws.st.rerun()
    for column in table_input.Columns:
        if column.Key not in dialog_values:
            value = row.get(column.Label)
            value = convert_value(column, value)
            dialog_values[column.Key] = value
        create_ui.build_input(gws, column, dialog_values, dialog="Edit")

    if gws.st.button("Submit"):
        update_df(table_input, dialog_values, selected_index)
        gws.st.rerun()

    process_dialog_inputs(table_input)


def convert_value(column, value):
    """Some values seem to the converted incorrectly this function fixes that
    Parameters
    ----------
    column
        model input for the column
    value
        Value to be tested and converted if needed
    Returns
    -------
    value
        Converted value"""
    if type(value) is float and math.isnan(value):
        value = None
        gws.st.session_state[column.Key] = value
    if column.Type == "integer_input" and value is not None:
        value = int(value)
        gws.st.session_state[column.Key] = value
        return value

    if column.Type == "checkbox" and value is not None:
        if type(value) is bool:
            ...
        elif value.lower() == "false" or value.lower() == "no" or value == "0":
            value = False
        elif value.lower() == "true" or value.lower() == "yes" or value == "1":
            value = True
        gws.st.session_state[column.Key] = value
        return value

    return value


def update_df(process_input, dialog_values, index=-1):
    """Convert they keys in the dialog from Key to code, update the dataframe"""
    key_mapping = {}
    for column in process_input.Columns:
        key_mapping[column.Key] = column.Label
    updated_data = {
        key_mapping.get(key, key): value for key, value in dialog_values.items()
    }
    df = gws.st.session_state[f"{process_input.Key}_df"]
    if index == -1:
        df.loc[len(df)] = updated_data
    else:
        df.loc[index] = updated_data


def process_dialog_inputs(table_input):
    if table_input.DialogInputs is not None:
        if "dialog_input_function" not in gws.st.session_state:
            function = construct_function(table_input.DialogInputs)
            gws.st.session_state["dialog_input_function"] = function
        else:
            function = gws.st.session_state["dialog_input_function"]
        if function is not None:
            function()
    else:
        gws.st.session_state["dialog_inputs"] = "all"
