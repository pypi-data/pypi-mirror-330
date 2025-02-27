import datetime
import json
import os
import pathlib
import platform
from typing import Any

import numpy
import streamlit as st
import yaml
from pathvalidate import is_valid_filepath

import gw_ui_streamlit.core as gws
from gw_ui_streamlit import constants, independant_utils
from gw_ui_streamlit.constants import KeyType
from gw_ui_streamlit.models import BaseConfig, UserInterface
import gw_ui_streamlit._utils as _utils


def codeify_string(input_string: str) -> str:
    """Converts the input to a unique code for the application
    :param input_string: str: The string to convert to a code"""
    return independant_utils.codeify_string(input_string)


def create_simple_key(key_type: KeyType, value: str) -> str:
    """Creates a simple key for the application
    :param key_type: KeyType: The type of key to create
    :param value: str: The value to add to the key"""
    gw_streamlit = st.session_state["GWStreamlit"]
    application = gw_streamlit.application
    key = codeify_string(input_string=f"{key_type.value}_{application}_{value}")
    return key


def _create_storage_key(value: str) -> str:
    """Creates a storage key for the application
    Storage keys enable the application to store information into the session
    :param value: str: The value to add to the key"""
    gw_streamlit = st.session_state["GWStreamlit"]
    application = gw_streamlit.application
    key = codeify_string(input_string=f"{KeyType.STORAGE.value}_{application}_{value}")
    return key


def read_yaml(yaml_file: str):
    """Reads the yaml file and returns the data
    :param yaml_file: str: The yaml file to read"""
    with open(yaml_file, "r") as file:
        yaml_data = yaml.safe_load(file)
        return yaml_data


def get_config_path(directory, file_name: str):
    """Returns the path to the configuration file depending on the operating system.
    Parameters
    ----------
    directory: str
        The directory to store the configuration file
    file_name: str
        The name of the configuration file"""
    if file_name.endswith(".json"):
        config_filename = file_name
    else:
        config_filename = f"{file_name}.json"
    if platform.system() == "Windows":
        # On Windows, it's typical to store config files in the AppData directory
        config_directory = os.path.join(os.getenv("APPDATA"), directory)
    elif platform.system() == "Darwin":
        # On macOS, it's typical to store config files in the Application Support directory
        user_directory = os.path.expanduser("~/Library/Application Support/")
        config_directory = os.path.join(user_directory, "Field Framework", directory)
    else:
        raise OSError("Unsupported operating system")

    if not os.path.exists(config_directory):
        os.makedirs(config_directory)  # Create the directory if it does not exist

    return os.path.join(config_directory, config_filename)


def disabled(item: BaseConfig) -> bool | None:
    """Check if the item is enabled
    Parameters
    ----------
    item: BaseConfig
        The item to check if it is enabled"""
    disabled_value = fetch_boolean(getattr(item, "immutable", False))
    if item.Enabled is not None:
        if st.session_state.get(_fetch_key(item.Enabled), None) is None:
            disabled_value = True
        else:
            disabled_value = False
    return disabled_value


def fetch_boolean(value):
    if type(value) is bool:
        return value
    if type(value) is str:
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False


def build_label(item: BaseConfig):
    """Construct the label for the UI
    Parameters
    ----------
    item: BaseConfig
        The ui item to build the label for"""
    if item.Required:
        return f"**{item.Label} :red[*]**"
    else:
        return f"**{item.Label}**"


def to_list(item_value) -> list:
    """Convert the item value to a list if it is not already a list
    Parameters
    ----------
    item_value: str
        Value to be converted to a list"""
    if type(item_value) is list:
        return item_value
    else:
        return [item_value]


def updated_edited_rows(df, edited_item):
    """Update the edited rows in dataframe
    Parameters
    ----------
    df: pandas.DataFrame
        dataframe to update
    edited_item
        The edited item to update"""
    for key, value in edited_item.items():
        for item_key, item_value in value.items():
            df.loc[key, item_key] = item_value
    return df


def update_data_editor(*, key: str, replace_values: dict):
    update_dataframe(key=key, update_rows=replace_values)


def update_dataframe(key: str, update_rows: dict):
    """Updates a dataframe, the dataframe should have been built and stored in self.data_frame
    The original rows are removed from the dataframe and the new rows are added. As there can be a missmatch in the
    index sizes this is the easiest way to perform the update of the dataframe. This function is only used to update
    the dataframe in the session_state from a saved configuration, otherwise the changes will be available in the
    streamlit data_edit component.
    :param key: The key used to store the dataframe in the session_state
    :param update_rows: The rows to be updated in the dataframe"""
    df_key = f"{key}_df"
    if st.session_state.get(df_key, None) is None:
        return

    st.session_state.get(df_key)

    original_index = st.session_state.get(df_key).index
    index_range = numpy.arange(original_index.start, original_index.stop).tolist()
    st.session_state.get(df_key).drop(index_range, inplace=True)
    for item in update_rows:
        st.session_state.get(df_key).loc[len(st.session_state.get(df_key))] = item
    st.session_state.get(df_key).reset_index(drop=True, inplace=True)


def _load_config(file_name):
    """Loads the session state with values from the configuration file
    :param file_name: str: The name of the configuration file"""
    gws = st.session_state["GWStreamlit"]
    if file_name is None:
        return
    if pathlib.Path(file_name).name == file_name:
        directory = codeify_string(input_string=gws.application)
        config_path = get_config_path(directory, file_name)
    else:
        config_path = file_name
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            update_session(config)
    except FileNotFoundError:
        return


def fetch_model_input(model_code):
    inputs = [item for item in gws.model().Inputs if item.Code == model_code]
    if len(inputs) == 0:
        return None
    if len(inputs) == 1:
        return inputs[0]
    if len(inputs) > 1:
        return None


def update_session(config: dict, *, using_code: bool = False):
    """Extracts the information from the config dict and populates the session state based on the keys
    Parameters
    ----------
    config: dict:
        The configuration to update the session state
    using_code: bool
        True the config will have short keys otherwise long keys"""
    for key, value in config.items():
        long_key = key
        if using_code:
            model_part = fetch_model_input(key)
            long_key = model_part.Key
        if str(long_key).startswith("input_") or str(long_key).startswith("table_"):
            if type(value) is list:
                update_data_editor(key=long_key, replace_values=value)
            else:
                st.session_state[long_key] = value


def build_key_dict(*, short_key: bool = False):
    """Build the key dictionary for the application
    :param short_key: bool: If True the short key is used, if False the long key is used as the key"""
    key_dict = {}
    gws = st.session_state["GWStreamlit"]
    for item in gws.model.Inputs:
        if short_key:
            key_dict[item.ShortKey] = item.Key
        else:
            key_dict[item.Key] = item.ShortKey
        for column in item.Columns:
            if short_key:
                key_dict[column.ShortKey] = column.Key
            else:
                key_dict[column.Key] = column.ShortKey
    return key_dict


def replace_short_key(section: str, short_key_config: dict):
    key_mapping = build_key_dict(short_key=True)
    data = short_key_config.get(section, None)
    result = replace_keys(data=data, key_mapping=key_mapping)
    return result

def replace_keys(data, key_mapping):
    """
    Replace keys in a nested dictionary or list with new keys provided in key_mapping.

    :param data: The original dictionary or list to modify.
    :param key_mapping: A dictionary mapping old keys to new keys.
    :return: The modified dictionary or list with keys replaced.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Replace the key if it exists in the key_mapping
            new_key = key_mapping.get(key, key)
            # Recursively replace keys in the value
            new_dict[new_key] = replace_keys(value, key_mapping)
        return new_dict

    elif isinstance(data, list):
        # Recursively replace keys in each item of the list
        return [replace_keys(item, key_mapping) for item in data]

    else:
        # If the value is neither a dict nor a list, return it as is
        return data


def _completed_required_fields() -> bool:
    """Show the required fields that are not filled
    :return: True if all required fields are filled, False if there are required fields that are not filled
    """
    required_list = []
    model = st.session_state["GWStreamlit"].model
    for input_field in [
        model_input for model_input in model.Inputs if model_input.Required
    ]:
        if input_field.Required and st.session_state.get(input_field.Key) is None:
            required_list.append(input_field.Label)
    if len(required_list) > 0:
        st.error(
            f"The following required fields are not filled: {', '.join(required_list)}"
        )
        return False
    return True


def _write_string(location, file_name, content, **kwargs):
    """Write a string to a file, there are multiple checks to ensure the file is written correctly
    If the path is invalid it will return an error message, if the contents to write are None it will return a message
    if the location is valid but does not exist it will be created.

    :param location: str: The location to write the file
    :param file_name: str: The name of the file
    :param content: str: The content to write to the file
    :param **kwargs: dict: Additional arguments to specify the package and extension
    """
    for key, value in kwargs.items():
        if key == "package":
            package_parts = value.split(".")
            for package_part in package_parts:
                location = os.path.join(location, package_part)
        if key == "extension":
            file_name = f"{file_name}.{value}"

    if content is None:
        _fetch_tab("Output").write(f"File content for: {location}/{file_name} is None")
        return
    if not is_valid_filepath(location, platform="auto"):
        _fetch_tab("Output").error("Source Location is an invalid path")
        return
    is_exist = os.path.exists(location)
    if not is_exist:
        os.makedirs(location)
        _fetch_tab("Output").write(f"Directory created: {location}")
    with open(f"{location}/{file_name}", "w") as file:
        file.write(content)
    _fetch_tab("Output").write(f"File created: {location}/{file_name}")


def _fetch_key(ui_item: Any, short_key: bool = False) -> str | None:
    """Fetch the key for the item, if the item is a string it will find the item in the model and return the key
    otherwise the key will be returned from the item
    :param ui_item: Model part or part identifier to fetch the key for"""
    if isinstance(ui_item, str):
        item_code = codeify_string(ui_item)
        gw_streamlit = st.session_state["GWStreamlit"]
        model_item = gw_streamlit.find_model_part(item_code)
        if model_item is None:
            return None
        return _fetch_key(model_item)
    else:
        if short_key:
            return ui_item.ShortKey
        else:
            return ui_item.Key


def build_model(yaml_file) -> UserInterface | None:
    """Build the model from the yaml file, and update to add the key and code if missing to the model
    :param yaml_file: The yaml file to build the model from"""
    if yaml_file is None:
        return None
    add_code(yaml_file)
    model = UserInterface.model_validate(yaml_file)
    return model


def add_code(ui_item, ui_type: str = None):
    """Add the code to the item if it is missing"""
    if ui_item.get("code") is None:
        if "label" in ui_item.keys():
            ui_item["code"] = capital_case(ui_item.get("label"))
        elif "name" in ui_item.keys():
            ui_item["code"] = capital_case(ui_item.get("name"))
        else:
            ui_item["code"] = capital_case(ui_item.get("unknown"))
    if ui_item.get("type") is None:
        ui_item["type"] = ui_type
    ui_item["key"] = build_key(ui_item, False)
    if ui_item.get("code") is None:
        ui_item["short_key"] = build_key(ui_item, True)
    else:
        ui_item["short_key"] = ui_item["code"]
    add_code_buttons(ui_item)
    add_code_inputs(ui_item)

    return ui_item

def add_code_buttons(ui_item):
    if "buttons" in ui_item.keys():
        for button in ui_item["buttons"]:
            add_code(button, "button")

def add_code_inputs(ui_item):
    if "inputs" in ui_item.keys():
        for input_field in ui_item["inputs"]:
            add_code(input_field)
            if "columns" in input_field.keys():
                for column in input_field["columns"]:
                    add_code(column)

def build_key(ui_item, short_key) -> str:
    ui_type = independant_utils.type_to_key_type(ui_item.get("type"))
    value = ui_item["code"]
    if short_key:
        key = independant_utils.codeify_string_title(value)
    else:
        gws = st.session_state["GWStreamlit"]
        application = gws.application
        key = independant_utils.codeify_string(input_string=f"{ui_type.value}_{application}_{value}")
    return key



def find_yaml_ui(yaml_file_name: str):
    templates = st.session_state.get(
        "templates", list_files(constants.YAML_UI_LOCATION, [".yaml", ".yml"])
    )
    yaml_object_list = [
        template for template in templates if template["code"] == yaml_file_name
    ]
    if len(yaml_object_list) == 0:
        yaml_object_list = [
            template for template in templates if template["name"] == yaml_file_name
        ]

    if len(yaml_object_list) == 0:
        st.session_state["template_selection"] = None
        return
    yaml_object = yaml_object_list[0]
    st.session_state["template_selection"] = yaml_object["name"]
    return yaml_object


def find_yaml_other(yaml_file_name: str):
    yaml_object = load_yaml(yaml_file_name)
    st.session_state["template_selection"] = yaml_object["name"]
    return yaml_object


def list_files(directory_path, file_types: list):
    found_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = pathlib.Path(file).suffix
            if file_extension in file_types:
                found_files.append(load_yaml(os.path.join(str(root), file)))

    return found_files


def load_yaml(file_path: str):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)



def _create_saved_state(*, short_key: bool = False):
    """Creates a saved state for the application
    Parameters
    ----------
    short_key : bool, optional
        If the saved state should save using the short code
    Returns
    -------
    dict
        Dictionary of the saved state"""
    interim_saved_dict = {}
    gws = st.session_state["GWStreamlit"]
    for item in gws.model.Inputs:
        if item.Key not in st.session_state.keys():
            continue
        value = st.session_state[item.Key]
        if short_key:
            save_key = item.Code
        else:
            save_key = item.Key
        interim_saved_dict[save_key] = process_key_value(item.Key, value)
    return interim_saved_dict


def get_save_key(gws, key, short_key):
    """Get the save key based on the short_key flag"""
    if short_key:
        model = gws.model
        if key.startswith("input_"):
            inputs = [item for item in model.Inputs if item.Key == key]
            if len(inputs) == 1:
                return inputs[0].ShortKey
        if key.startswith("table_"):
            inputs = [item for item in model.Inputs if item.Key == key]
            if len(inputs) == 1:
                return inputs[0].ShortKey
    return key


def process_key_value(key, value):
    """Process the key value based on its type"""
    if key.startswith("input_"):
        if isinstance(value, datetime.date):
            return value.isoformat()
        return value
    if key.startswith("table_"):
        if key.endswith("_df"):
            return None
        if f"{key}_df" in st.session_state:
            return process_dataframe(key)
    if key.startswith("storage_"):
        return value
    return None


def process_dataframe(key):
    """Process the dataframe for the given key"""
    df = st.session_state[f"{key}_df"]
    for del_index in to_list(st.session_state[key].get("deleted_rows", [])):
        df.drop(del_index, inplace=True)
    for added_item in to_list(st.session_state[key].get("added_rows", [])):
        if added_item:
            df.loc[len(df)] = added_item
    for edited_item in to_list(st.session_state[key].get("edited_rows", [])):
        if edited_item:
            updated_edited_rows(df, edited_item)
    df.reset_index(drop=True, inplace=True)
    return df.to_dict("records")


def _fetch_configs(application_name: str):
    """List of saved configurations for the application"""
    file_list = []
    directory = codeify_string(application_name)
    config_path = get_config_path(directory, "temp.json")
    for root, dirs, files in os.walk(os.path.dirname(config_path)):
        for file in files:
            if file.endswith(".json"):
                file_list.append(file)
    return file_list


def _save_config(application_name: str, file_name, config_data):
    """Saves the given configuration data to a JSON file."""
    if file_name is None:
        return
    directory = codeify_string(application_name)
    config_path = get_config_path(directory, file_name)
    with open(config_path, "w") as file:
        json.dump(config_data, file, indent=4)


def _fetch_tab(item: Any):
    if isinstance(item, str):
        tab = st.session_state["GWStreamlit"].tab_dict.get(item)
    else:
        tab_name = item.Tab
        if tab_name is None:
            tab_name = "Main"
        gws = st.session_state["GWStreamlit"]
        if gws.child is None:
            tab = gws.tab_dict.get(tab_name)
        else:
            tab = gws.child.tab_dict.get(tab_name)
    return tab


def _save_storage(key, value: Any):
    if key is None:

        return

    if key in st.session_state.keys():
        st.session_state[key] = value


def _show_info(message, tab=None):
    if tab is None:
        tab = "Output"
    _fetch_tab(tab).info(message)


def _show_warning(message, tab=None):
    if tab is None:
        tab = "Output"
    _fetch_tab(tab).warning(message)


def _show_error(message, tab=None):
    if tab is None:
        tab = "Output"
    _fetch_tab(tab).error(message)


def capital_case(value: str) -> str:
    return independant_utils.capital_case(value)


def construct_function(function_name):
    defined_function = _utils.construct_function(function_name)
    return defined_function


def cache_item(item):
    if item.Cache:
        gws.cache().set(item.Key, gws.st.session_state[item.Key])
        gws.cache().set(item.ShortKey, gws.st.session_state[item.Key])
        gws.cache().set(item.Code, gws.st.session_state[item.Key])

