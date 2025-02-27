from typing import Any
import json

import pandas
import streamlit as st
from pathlib import Path

import gw_ui_streamlit._create_ui as gwu
from gw_ui_streamlit._utils import build_default_rows
from gw_ui_streamlit.cache import GWSCache
from gw_ui_streamlit.create_ui import build_columns, build_dataframe
from gw_ui_streamlit.dialog_ui import (
    table_row_add_dialog,
    table_row_edit_dialog,
    process_dialog_inputs,
)
from gw_ui_streamlit.models import UserInterface, InputFields
from gw_ui_streamlit.process_templates import _process_template_by_name
from gw_ui_streamlit.utils import (
    find_yaml_ui,
    find_yaml_other,
    build_model,
    _fetch_key,
    _fetch_configs,
    _completed_required_fields,
    _create_saved_state,
    _save_config,
    _load_config,
    _write_string,
    _fetch_tab,
    _create_storage_key,
    _show_info,
    _show_warning,
    _show_error,
    codeify_string,
)


class GWStreamlit:

    def create_ui(self):
        """Builds the UI for the application"""
        if self.built_ui:
            return
        gwu.create_ui_title(self)
        gwu.create_ui_buttons(self)
        if not self.model.Title:
            gwu.create_ui_tabs(self)
        gwu.create_tab_buttons(self)
        gwu.create_ui_inputs(self)
        self.built_ui = True

    def find_model_part(self, identifier: str) -> None | InputFields:
        """Finds a model part by the identifier provided. The identifier can be the code or the
        label of the item. If the item is not found None is returned.
        Parameters
        ----------
        identifier: str
            Identifier of the item to find"""
        items = [item for item in self.model.Inputs 
            if codeify_string(item.Code) == codeify_string(identifier)
        ]
        if len(items) == 0:
            items = [item for item in self.model.Inputs if item.Label == identifier]
        if len(items) == 0:
            return None
        return items[0]

    def __init__(
        self,
        application: str = None,
        yaml_file: dict = None,
        *,
        single_application: bool = False,
    ):
        self.application = application
        self.yaml_file = yaml_file
        self.model = build_model(self.yaml_file)
        self.keys = []
        self.input_values = {}
        self.button_values = {}
        self.built_ui = False
        self.tab_dict = {}
        self.default_rows = build_default_rows(self)
        self.child = None
        self.saved_state: dict
        self.modal = False
        self.cache = GWSCache()
        self.single_application = single_application

    def populate(
        self,
        application: str = None,
        yaml_file: dict = None,
        *,
        single_application: bool = False,
    ):
        """Populates the GWStreamlit object with the application and yaml file

        Parameters
        ----------
        application : str, optional
            Application Code to use, by default None
        yaml_file : dict, optional
            yaml file code or the path to a yaml file, by default None
        single_application : bool, optional
            Indicates that this constitues a single application of one or more pages
            If True, the application will not be reset when the user navigates to another page*
        """
        self.application = application
        self.yaml_file = yaml_file
        self.model = build_model(self.yaml_file)
        self.default_rows = build_default_rows(self)
        self.built_ui = False
        gwu.discover_functions(self)


def initialize(application: str, yaml_file_name: str, *, single_application: bool = False):
    """Initializes the application
    Parameters
    ----------
    application : str
        Name of the application
    yaml_file_name : str
        Name of the yaml file, if file is not in the default location then this needs to be the full path
    """
    if Path(yaml_file_name).name == yaml_file_name:
        yaml_file = find_yaml_ui(yaml_file_name)
    else:
        yaml_file = find_yaml_other(yaml_file_name)
    st.session_state["GWStreamlit"].populate(
        application, yaml_file, single_application=single_application
    )
    st.session_state["GWStreamlit"].create_ui()


def cache() -> GWSCache:
    gws = st.session_state["GWStreamlit"]
    return gws.cache


def required_fields() -> bool:
    """Checks if all required fields have been completed"""
    return _completed_required_fields()


def fetch_key(ui_item: Any) -> str:
    """Fetches the key for the item provided"""
    return _fetch_key(ui_item)


def fetch_configs(application_name: str = None) -> list:
    """Extract the configurations for the application"""
    if application_name is None:
        application_name = st.session_state["GWStreamlit"].application
    return _fetch_configs(application_name)


def create_saved_state(*, short_key: bool = False):
    """Creates a saved state for the application"
    Parameters
    ----------
    short_key : bool, optional
        If True, creates a short key for the saved state"""
    return _create_saved_state(short_key=short_key)


def save_config(file_name, config_data: None):
    """Save the configuration information"""
    if config_data is None:
        config_data = create_saved_state()
    application_name = st.session_state["GWStreamlit"].application
    _save_config(application_name, file_name, config_data)


def load_config(file_name):
    """Loads a configuration file"""
    _load_config(file_name)


def process_template_by_name(template_name, input_dict: dict, location="resources/templates"):
    """Processes a template by name"""
    return _process_template_by_name(template_name, input_dict, location)


def write_string(location, file_name, content, **kwargs):
    """Writes a string to a file"""
    _write_string(location, file_name, content, **kwargs)


def write_json(location, file_name, content, **kwargs):
    """Writes json to a file"""
    string_content = json.dumps(content)
    _write_string(location, file_name, string_content, **kwargs)


def fetch_tab(item: Any):
    """Fetches a tab by the item provided"""
    return _fetch_tab(item)


def create_storage_key(key_value: str) -> str:
    """Creates a storage key for the value provided"""
    return _create_storage_key(key_value)


def generate_image(item):
    gws = st.session_state["GWStreamlit"]
    gwu.generate_image(gws, item)


def find_model_part(identifier: str):
    gws = st.session_state["GWStreamlit"]
    return gws.find_model_part(identifier)


def show_info(message, tab="Output"):
    """Displays an information message on the UI, optionaly a tab can be define,
    by default it will display on the Output Tab

    Parameters
    ----------
    message
        Text to display
    tab (optional)
        tab to where the message will be displayed
    """
    _show_info(message, tab)


def show_warning(message, tab="Output"):
    _show_warning(message, tab)


def show_error(message, tab="Output"):
    _show_error(message, tab)


def model() -> UserInterface:
    gws = st.session_state["GWStreamlit"]
    return gws.model


def model_inputs() -> list[InputFields]:
    gws = st.session_state["GWStreamlit"]
    return gws.model.Inputs


def value(identifier: str):
    item = find_model_part(identifier)
    if item is None:
        key = create_storage_key(identifier)
        return st.session_state.get(key)
    else:
        return st.session_state.get(item.Key)


def save_storage(key, storage_value: Any):
    key = create_storage_key(key)
    st.session_state[key] = storage_value


def fetch_value(*, key: str = None, name: str = None):
    """Extract the value from the session state, if there is no key that corresponds to the name
    supplied the cache is interrogated for the key and value"""
    if key is None:
        key = fetch_key(name)
    item_value = st.session_state.get(key)
    if item_value is None:
        gws = st.session_state["GWStreamlit"]
        if gws.cache.has_key(key):
            item_value = gws.cache.get(name)
    return item_value


def fetch_value_reset(*, key: str = None, name: str = None):
    return_value = fetch_value(key=key, name=name)
    if key is not None:
        st.session_state[key] = None
    return return_value


def set_value(name: str, input_value):
    """Sets the value in either the session state or in the cache, if the name provided matched a key in
    the session state it is updated with the value, otherwise the cache is updated"""
    if name in st.session_state:
        st.session_state[name] = input_value
    else:
        gws = st.session_state["GWStreamlit"]
        gws.cache.set(name, input_value)


def get_model() -> UserInterface:
    """Returns the model for the application"""
    return st.session_state["GWStreamlit"].model


def add_table_row_dialog(table_code: str):
    dialog_values = {}
    model = get_model()
    process_input = next(
        (item for item in model.Inputs if item.Code == table_code and item.Type == "table"),
        None,
    )
    if process_input is not None:
        for column in process_input.Columns:
            st.session_state[column.Key] = None
    # cache().set("InputType", "text_input")
    table_row_add_dialog(process_input, dialog_values)


def edit_table_row_dialog(table_code: str):
    dialog_values = {}
    key = fetch_key(table_code)
    selected = st.session_state[key].selection
    if selected is None or len(selected["rows"]) == 0:
        return
    selected_index = selected["rows"][0]
    df = st.session_state[f"{key}_df"]
    row = df.iloc[selected_index].to_dict()
    model = get_model()
    process_input = None
    for model_input in model.Inputs:
        if model_input.Type == "table" and model_input.Code == table_code:
            process_input = model_input
    for column in process_input.Columns:
        st.session_state[column.Key] = row.get(column.Label)
    table_row_edit_dialog(process_input, row, selected_index, dialog_values)


def reset_inputs():
    """Resets the inputs on the UI, most inputs will be reset to None. Tables will have the contents
    of the dataframe erased and recreated with the default values if they exist
    """
    gws = st.session_state["GWStreamlit"]
    for model_input in get_model().Inputs:
        if model_input.Type != "table":
            st.session_state[model_input.Key] = None
        else:
            if model_input.DefaultFunction:
                defined_function = model_input.DefaultFunctionBuilt
                default_rows = defined_function()
            else:
                default_rows = gws.default_rows.get(model_input.Label, dict())
            columns = build_columns(model_input)
            st.session_state[model_input.Key]["deleted_rows"] = []
            st.session_state[model_input.Key]["added_rows"] = []
            st.session_state[model_input.Key]["edited_rows"] = []

            df = st.session_state[f"{model_input.Key}_df"]
            df.drop(list(df.index.values), inplace=True)

            for default in default_rows:
                df.loc[len(df)] = default
            df.reset_index(drop=True, inplace=True)
