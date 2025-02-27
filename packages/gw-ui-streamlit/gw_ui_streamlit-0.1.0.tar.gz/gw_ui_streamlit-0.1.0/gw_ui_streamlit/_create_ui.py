from typing import Optional

import pandas as pd
import streamlit as st

from gw_ui_streamlit._utils import construct_function
from gw_ui_streamlit.constants import ButtonLevel, DEFAULT_DATE_FORMAT
from gw_ui_streamlit.models import BaseConfig, InputFieldsBase
from gw_ui_streamlit.utils import disabled, build_label, fetch_boolean, _fetch_tab, cache_item
from streamlit import dialog


def create_ui_tabs(gws):
    """Creates a list of tabs to be used in the UI
    Parameters
    ----------
    gws
        The GWS Core"""
    tab_dict = {item.Tab: None for item in gws.model.Inputs if item.Tab is not None}
    if len([item for item in gws.model.Inputs if item.Tab is None]) > 0:
        tab_dict["Main"] = None

    for tab in gws.model.Tabs:
        tab_dict[tab.Label] = None
    tab_dict["Output"] = None

    tabs = st.tabs(tab_dict.keys())
    tab_position = 0

    for tab in tab_dict.keys():
        tab_dict[tab] = tabs[tab_position]
        tab_position += 1
    gws.tab_dict = tab_dict


def create_ui_title(gws):
    """Creates a title for the UI page and a description if it exists in the YAML file.
    If the title exists in the yaml file no buttons are generated.
    Parameters
    ----------
    gws
        The GWS Core"""
    try:
        st.header(gws.model.Name, divider="blue")
        if gws.model.Description is not None:
            st.markdown(gws.model.Description)
        if gws.model.Concept is not None:
            st.write(f"Concept by: {gws.model.Concept}")
        if gws.model.Developer is not None:
            st.write(f"Developed by: {gws.model.Developer}")
    except Exception as e:
        st.exception(e)


def discover_functions(gws):
    """Discovers the functions in the YAML file, the functions are constructed and stored in the
    appropriate location in the model
    Parameters
    ----------
    gws
        The GWS Core"""
    for button in [item for item in gws.model.Buttons]:
        discover_function(gws, button)

    for input_item in [item for item in gws.model.Inputs]:
        discover_function(gws, input_item)
        if input_item.Type == "table":
            for column_item in input_item.Columns:
                discover_function(gws, column_item)


def discover_function(gws, item):
        """Discovers the functions in the YAML file, the functions are constructed and stored in the
        appropriate location in the model
        Parameters
        ----------
        gws
            The GWS Core"""
        item.OnClickFunction = construct_function(item.OnClick)

        item.OnChangeFunction = construct_function(item.OnChange)
        if item.OnSelect is not None:
            if item.OnSelect not in ["ignore", "rerun"]:
                item.OnSelectFunction = construct_function(item.OnSelect)
        if item.DefaultFunction is not None:
            item.DefaultFunctionBuilt = construct_function(item.DefaultFunction)
        if item.InputOptions is not None and (
                len(item.InputOptions) == 1
                and item.InputOptions[0].Function is not None
        ):
            function_name = item.InputOptions[0].Function
            item.InputOptions[0].OptionsFunction = construct_function(function_name)


def create_ui_buttons(gws):
    """Generates a set of buttons based on the YAML file provided
    Parameters
    ----------
    gws
        The GWS Core"""
    with st.container():
        columns = st.columns([1, 1, 1, 1, 1])
        column_index = 0
        for button in [
            item for item in gws.model.Buttons if item.Level is not ButtonLevel.tab
        ]:
            with columns[column_index]:
                try:
                    on_click = button.OnClickFunction
                    if button.Icon is None:
                        icon = None
                    else:
                        icon = f":material/{button.Icon}:"
                    st.button(
                        f"{button.Label}",
                        key=button.Key,
                        on_click=on_click,
                        type=button.Variant.value,
                        use_container_width=True,
                        icon=icon
                    )
                except Exception as e:
                    st.exception(e)
            column_index += 1


def create_tab_buttons(gws):
    """Generates a set of buttons based on the YAML file provided
    Parameters
    ----------
    gws
        The GWS Core"""
    button_tab_list = [
        item.Tab for item in gws.model.Buttons if item.Level == ButtonLevel.tab
    ]
    button_tab_list = list(set(button_tab_list))  # Remove the duplicates
    if len(button_tab_list) == 0:
        return
    for tab in button_tab_list:
        with _fetch_tab(tab):
            with st.empty():
                with st.container():
                    columns = st.columns([1, 1, 1, 1, 1])
                    column_index = 4
                    button_list = [
                        item
                        for item in gws.model.Buttons
                        if item.Tab == tab and item.Level == ButtonLevel.tab
                    ]
                    for button in list(reversed(button_list)):
                        with columns[column_index]:
                            if button.Icon is None:
                                icon = None
                            else:
                                icon = f":material/{button.Icon}:"
                            on_click = construct_function(button.OnClick)
                            st.button(
                                f"{button.Label}",
                                key=button.Key,
                                on_click=on_click,
                                type=button.Variant.value,
                                use_container_width=True,
                                icon=icon
                            )
                        column_index -= 1


def create_table_buttons(*, gws, table_item, dialog=None, location):
    """Generates a set of buttons based on the YAML file provided
    Parameters
    ----------
    gws
        The GWS Core"""
    columns = st.columns([1, 1, 1, 1, 1])
    column_index = 4
    button_list = [
        item
        for item in table_item.Buttons if item.Level == ButtonLevel.table
    ]
    for button in list(reversed(button_list)):

        with columns[column_index]:
            if button.Icon is None:
                icon = None
            else:
                icon = f":material/{button.Icon}:"
            on_click = construct_function(button.OnClick)
            st.button(
                f"{button.Label}",
                key=button.Key,
                on_click=on_click,
                type=button.Variant.value,
                use_container_width=True,
                icon=icon
            )
        column_index -= 1


def create_ui_inputs(gws):
    """Main processing for the inputs defined in the yaml file. Each type of input
    is handled separately. Each input has a key generated that corresponds to the label or code
    and the state name defined in the main module for the application
    Parameters
    ----------
    gws
        The GWS Core"""
    if gws.model.Inputs is None:
        return
    for ui_item in gws.model.Inputs:
        build_input(gws, ui_item, gws.input_values)


def build_input(gws, ui_item, storage_dict, *, dialog=None, location=None):
    """Main processing for the inputs defined in the yaml file. Each type of input
    is handled separately. Each input has a key generated that corresponds to the label or code
    and the state name defined in the main module for the application
    Parameters
    ----------
    gws
        The GWS Core
    ui_item
        The yaml ui item to process
    storage_dict
        The storage dictionary to use
    dialog
        Indicator asto the type of UI(dialog or standard)"""

    if ui_item.Key not in storage_dict.keys():
        storage_dict[ui_item.Key] = None

    if ui_item.Type == "text_input":
        generate_text_input(gws, ui_item, storage_dict, dialog=dialog, location=location)

    if ui_item.Type == "code_input":
        generate_text_input(gws, ui_item, storage_dict, dialog=dialog, code_input=True, location=location)

    if ui_item.Type == "text_area":
        generate_text_input(gws, ui_item, storage_dict, text_area=True, dialog=dialog, location=location)

    if ui_item.Type == "date_input":
        generate_date_input(gws, ui_item, storage_dict, dialog=dialog, location=location)

    if ui_item.Type == "selectbox":
        generate_selectbox(gws, ui_item, storage_dict, dialog=dialog, location=location)

    if ui_item.Type == "image":
        generate_image(gws, ui_item, dialog=dialog, location=location)

    if ui_item.Type == "checkbox":
        generate_checkbox(gws, ui_item, storage_dict, dialog=dialog, location=location)

    if ui_item.Type == "toggle":
        generate_checkbox(gws, ui_item, storage_dict, toggle=True, dialog=dialog, location=location)

    if ui_item.Type == "integer_input":
        generate_integer_input(gws, ui_item, storage_dict, dialog=dialog, location=location)

    if ui_item.Type == "file_upload":
        generate_file_upload(gws, ui_item, storage_dict, dialog=dialog, location=location)

    if ui_item.Type == "multiselect":
        generate_selectbox(gws, ui_item, storage_dict, multiselect=True, dialog=dialog, location=location)

    if ui_item.Type == "table":
        generate_table(gws, ui_item, location=location)

    return ui_item.Key


def generate_text_input(gws, item, storage_dict, *, text_area=False, dialog=None, code_input=False, location=None):
    """text input processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in
    the YAML file.
    Parameters
    ----------
    gws
        The GWS Core
    item
        The yaml item to process
    storage_dict
        The storage dictionary to use
    text_area : bool
        If the text input will be a text_area
    dialog
        Indicator asto the type of UI(dialog or standard)
    code_input : bool
        If the text input will be a code_input, this will perform conversion on the string to codify it"""
    default_value = item.Default
    if item.DefaultFunction:
        defined_function = item.DefaultFunctionBuilt
        default_value = defined_function()

    if storage_dict.get(item.Key) is not None and (dialog is None or dialog == "Edit"):
        default_value = storage_dict[item.Key]

    on_change = item.OnChangeFunction
    if code_input:
        on_change = code_format(item)
    disabled_input = disabled(item)
    st_location = get_location(gws=gws, dialog=dialog, item=item, location=location)
    if item.Key not in st.session_state.keys():
        st.session_state[item.Key] = default_value
    try:
        if text_area:
            storage_dict[item.Key] = st_location.text_area(
                build_label(item),
                key=item.Key,
                on_change=on_change,
                disabled=disabled_input,
                help=item.Help,
            )
        else:
            storage_dict[item.Key] = st_location.text_input(
                build_label(item),
                key=item.Key,
                on_change=on_change,
                disabled=disabled_input,
                help=item.Help,
            )
        cache_item(item)
    except Exception as e:
        st.write(e)


def generate_date_input(gws, item, storage_dict, *, dialog=None, location=None):
    """date_input processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in
    the YAML file.
    Parameters
    ----------
    gws
        The GWS Core
    item
        The yaml item to process
    storage_dict
        The storage dictionary to use
    dialog
        Indicator asto the type of UI(dialog or standard)"""
    default_value = item.Default
    if item.DefaultFunction:
        defined_function = item.DefaultFunctionBuilt
        default_value = defined_function()

    if storage_dict.get(item.Key) is not None and (dialog is None or dialog == "Edit"):
        default_value = storage_dict[item.Key]

    on_change = item.OnChangeFunction
    disabled_input = disabled(item)
    date_format = item.DateFormat
    if date_format is None:
        date_format = DEFAULT_DATE_FORMAT
    if item.Key not in st.session_state.keys():
        st.session_state[item.Key] = default_value

    st_location = get_location(gws=gws, dialog=dialog, item=item, location=location)
    try:
        storage_dict[item.Key] = st_location.date_input(
            build_label(item),
            key=item.Key,
            on_change=on_change,
            disabled=disabled_input,
            help=item.Help,
            format=date_format,
        )
        cache_item(item)
    except Exception as e:
        st.write(e)
    if item.ShortKey in st.session_state.get("common_storage", {}):
        st.session_state["common_storage"][item.ShortKey] = st.session_state[item.Key]


def generate_image(gws, item, dialog=None):
    if item.Image is not None:
        if dialog is None:
            location = gws.st
        else:
            location = _fetch_tab(item)
        caption = f"{build_label(item)} - {item.Image}"
        location.image(item.Image, caption=caption)


def generate_checkbox(gws, item: BaseConfig, storage_dict, *, toggle=False, dialog=None, location=None):
    """Check Box Processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in the
    YAML file.
    Parameters
    ----------
    gws
        The GWS Core
    item
        The yaml item to process
    storage_dict
        The storage dictionary to use
    toggle
        Indicator asto the type of widget, checkbox or toggle
    dialog
        Indicator asto the type of UI(dialog or standard)"""
    if item.Default is None:
        default_value = False
    else:
        default_value = item.Default
    if item.DefaultFunction:
        defined_function = item.DefaultFunctionBuilt
        default_value = defined_function()
    if storage_dict.get(item.Key) is not None and (dialog is None or dialog == "Edit"):
        default_value = storage_dict[item.Key]
    on_change = item.OnChangeFunction
    disabled_input = disabled(item)
    st_location = get_location(gws=gws, dialog=dialog, item=item, location=location)
    if item.Key not in st.session_state.keys() or (default_value is not None and st.session_state[item.Key] is None):
        st.session_state[item.Key] = default_value
    try:
        if not toggle:
            storage_dict[item.Key] = st_location.checkbox(
                build_label(item),
                key=item.Key,
                on_change=on_change,
                disabled=disabled_input,
            )
        else:
            storage_dict[item.Key] = st_location.toggle(
                build_label(item),
                key=item.Key,
                on_change=on_change,
                disabled=disabled_input,
            )
        cache_item(item)
    except Exception as e:
        st.write(e)


def generate_file_upload(gws, item, storage_dict, *, dialog=None, location=None):
    """File Upload Processing. The extension is used to set the type of file that can be uploaded.
    The on_change function is constructed based on the name provided in the YAML file.
    The input is disabled if the immutable flag is set in the YAML file.
    Parameters
    ----------
    gws
        The GWS Core
    item
        The yaml item to process
    storage_dict
        The storage dictionary to use
    dialog
        Indicator asto the type of UI(dialog or standard)"""
    st_location = get_location(gws=gws, dialog=dialog, item=item, location=location)
    try:
        on_change = item.OnChangeFunction
        storage_dict[item.Key] = st_location.file_uploader(
            build_label(item),
            type=item.Extension,
            accept_multiple_files=False,
            key=item.Key,
            on_change=on_change,
            help=item.Help,
        )
        cache_item(item)
    except Exception as e:
        st.write(e)


def generate_integer_input(gws, item: InputFieldsBase, storage_dict, *, dialog=None, location=None):
    """Integer Input Processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in the
    YAML file. The min and max values are used to set the range of the input."""

    # default_value = item.Default
    # if item.DefaultFunction:
    #     defined_function = item.DefaultFunctionBuilt
    #     default_value = defined_function()
    #
    # if storage_dict.get(item.Key) is not None and (dialog is None or dialog == "Edit"):
    #     default_value = storage_dict[item.Key]

    on_change = item.OnChangeFunction
    disabled_input = disabled(item)

    if dialog is not None:
        location = gws.st
    else:
        location = _fetch_tab(item)

    if item.Min:
        min_value = item.Min
    else:
        min_value = 0

    if item.Max:
        max_value = item.Max
    else:
        max_value = 100

    st_location = get_location(gws=gws, dialog=dialog, item=item, location=location)

    try:
        on_change = item.OnChangeFunction
        disabled_field = fetch_boolean(item.Immutable)
        storage_dict[item.Key] = st_location.number_input(
            build_label(item),
            key=item.Key,
            step=1,
            min_value=min_value,
            max_value=max_value,
            on_change=on_change,
            disabled=disabled_field,
            help=item.Help,
        )
        cache_item(item)
    except Exception as e:
        st.write(e)


def generate_selectbox(gws, item: BaseConfig, storage_dict, *, multiselect=False, dialog=None, location=None):
    """select box processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in the
    YAML file.
    If the options are defined as a function the function is called to get the options. If the default value is not
    in the options list the first option is used as the default value."""
    options_dict = options_list(item)
    options = options_dict.get("options")
    default_value = options_dict.get("default_value")
    on_change = item.OnChangeFunction
    if options is not None and len(options) > 0 and default_value is not None:
        index_value = options.index(default_value)
    else:
        index_value = None
    disabled_field = fetch_boolean(item.Immutable)
    if item.Key in storage_dict.keys():
        st.session_state[item.Key] = st.session_state.get(item.Key)
    if st.session_state.get(item.Key) is None and default_value is not None:
        st.session_state[item.Key] = default_value

    st_location = get_location(gws=gws, dialog=dialog, item=item, location=location)

    try:
        if multiselect:
            storage_dict[item.Key] = st_location.multiselect(
                build_label(item),
                options,
                key=item.Key,
                on_change=on_change,
                disabled=disabled_field,
                help=item.Help,
            )
        else:
            storage_dict[item.Key] = st_location.selectbox(
                build_label(item),
                options,
                index=index_value,
                key=item.Key,
                on_change=on_change,
                disabled=disabled_field,
                help=item.Help,
            )
        cache_item(item)
    except Exception as e:
        st.write(e)


def generate_table(gws, item, *, dialog=None, location=None):
    """Main Processing for table generation. Each table is backed by a dataframe that is stored
    in self.data_frame."""

    if item.DefaultFunction:
        defined_function = item.DefaultFunctionBuilt
        default_rows = defined_function()
    else:
        default_rows = gws.default_rows.get(item.Label, dict())
    # with st.container():
    #     if item.Buttons:
    #         create_table_buttons(gws=gws, table_item=item, location=_fetch_tab(item))
    st_location = generate_dataframe(gws, item, default_rows)


def build_columns(item):
    if item.Columns[0].Function is not None:
        defined_function = construct_function(item.Columns[0].Function)
        columns = defined_function()
    else:
        columns = [entity_item.Label for entity_item in item.Columns]
    return columns


def build_dataframe(item, columns, default_rows):
    df = pd.DataFrame(columns=columns, data=default_rows)
    if item.Order:
        df.sort_values(by=[item.Order], inplace=True, ignore_index=True)
    return df


def generate_dataframe(gws, item: InputFieldsBase, default_rows: dict):
    """Generate the Table Dataframe. The default rows are used to populate the dataframe if it is empty. The columns
    are generated based on the YAML file provided. The dataframe is stored in self.data_frame and can be updated
    Parameters
    ----------
    gws
        Core GWS Class
    item: InputFieldsBase
        Input fields class
    default_rows
        Default rows dictionary
    """
    if item.Columns is None:
        return

    columns = build_columns(item)


    df_key = f"{item.Key}_df"
    if df_key in st.session_state.keys():
        df = st.session_state[df_key]
    else:
        df = build_dataframe(item, columns, default_rows)

    column_config = create_column_config(item.Columns)
    column_order = [column.Label for column in item.Columns if column.Hidden == False]
    _fetch_tab(item).markdown(f"**{item.Label}**")
    if item.OnSelectFunction is not None:
        select_function = item.OnSelectFunction
    else:
        select_function = item.OnSelect
    st.session_state[df_key] = df
    try:
        if item.Immutable:
            _fetch_tab(item).dataframe(
                st.session_state[df_key],
                hide_index=True,
                column_config=column_config,
                use_container_width=True,
                key=item.Key,
                selection_mode=item.SelectionMode,
                on_select=select_function,
                column_order=column_order,
            )
            gws.cache.set(item.Key, st.session_state[item.Key].selection)
        else:
            _fetch_tab(item).data_editor(
                st.session_state[df_key],
                num_rows="dynamic",
                column_config=column_config,
                use_container_width=True,
                key=item.Key,
            )
        cache_item(item)
    except Exception as e:
        st.write(e)


def create_column_config(columns: list[InputFieldsBase]):
    """Define the column configuration for the data editor, multiselect is not supported in the data editor and
    list column is used"""
    column_config = {}
    for column_item in columns:
        column = column_item.Label
        if column is None:
            column = column_item
        if column_item.InputOptions:
            options_dict = options_list(column_item)
            options = options_dict.get("options")
            default_value = options_dict.get("default_value")
            column_config[column] = st.column_config.SelectboxColumn(
                options=options, default=default_value
            )
        create_column_config_checkbox(column, column_item, column_config)
        create_column_config_date_input(column, column_item, column_config)
        create_column_config_integer_input(column, column_item, column_config)
        create_column_config_multiselect(column, column_item, column_config)
    return column_config


def create_column_config_multiselect(column, column_item, column_config):
    if column_item.Type == "multiselect":
        column_config[column] = st.column_config.ListColumn()


def create_column_config_checkbox(column, column_item, column_config):
    if column_item.Type == "checkbox":
        column_config[column] = st.column_config.CheckboxColumn(default=False)


def create_column_config_date_input(column, column_item, column_config):
    if column_item.Type == "date_input":
        date_format = column_item.DateFormat
        if date_format is None:
            date_format = DEFAULT_DATE_FORMAT
        column_config[column] = st.column_config.DatetimeColumn(format=date_format)


def create_column_config_integer_input(column, column_item, column_config):
    if column_item.Type == "integer_input":
        if column_item.Min is None:
            min_value = 0
        else:
            min_value = column_item.Min
        if column_item.Max is None:
            max_value = 100
        else:
            max_value = column_item.Min
        column_config[column] = st.column_config.NumberColumn(
            max_value=max_value, min_value=min_value, step=1, default=-1
        )


def options_list(item):
    if item.InputOptions is None:
        return {}
    defined_option_function = item.InputOptions[0].OptionsFunction
    default_value: Optional[str] = item.Default
    if defined_option_function is None:
        options = [option.Value for option in item.InputOptions]
        if item.Default not in options:
            default_value = item.InputOptions[0].Value
    else:
        options = defined_option_function()
    return {"options": options, "default_value": default_value}


def code_format(item):
    if item.Key in st.session_state.keys():
        code_value = st.session_state[item.Key]
        if code_value:
            st.session_state[item.Key] = code_value.lower().replace(" ", "_")


def get_location(*, gws, dialog=None, item=None, location=None):
    if location is not None:
        return location
    if dialog is not None:
        return gws.st
    else:
        return _fetch_tab(item)
