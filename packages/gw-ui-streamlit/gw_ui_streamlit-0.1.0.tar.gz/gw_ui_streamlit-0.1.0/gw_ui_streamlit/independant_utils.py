import re

from gw_ui_streamlit.constants import KeyType, LOCAL_DBM_LOCATION


def codeify_string(input_string: str):
    """Codeify a string, removing spaces and replacing with underscores
    Parameters
    ----------
    input_string : str
        Original string to codify"""
    if input_string is None:
        return None
    new_string = input_string.replace(' ', '_').lower().replace("_/_", "_")
    return new_string

def codeify_string_title(input_string: str):
    """Codeify a string, removing spaces and replacing with underscores, this results in title case that
    is more readable than the default codeify_string
    Parameters
    ----------
    input_string : str
        Original string to codify"""
    new_string = capital_case(input_string)
    new_string = new_string.replace("&", "And")
    new_string = new_string.replace(' ', '')
    new_string = new_string.replace("_","")
    return new_string


def type_to_key_type(yaml_type) -> KeyType:
    """Identifies the type of key prefix for the ui type
    Parameters
    ----------
    yaml_type : str
        Type of input
    Returns
    -------
    KeyType
        The Key Type Enum corresponding to the yaml type"""
    if yaml_type == "text_input":
        return KeyType.INPUT
    if yaml_type == "text_area":
        return KeyType.INPUT
    if yaml_type == "code_input":
        return KeyType.INPUT
    if yaml_type == "integer_input":
        return KeyType.INPUT
    elif yaml_type == "button":
        return KeyType.BUTTON
    elif yaml_type == "tab":
        return KeyType.TAB
    elif yaml_type == "storage":
        return KeyType.STORAGE
    elif yaml_type == "table":
        return KeyType.TABLE
    elif yaml_type == "selectbox":
        return KeyType.INPUT
    elif yaml_type == "checkbox":
        return KeyType.INPUT
    elif yaml_type == "date_input":
        return KeyType.INPUT
    else:
        return KeyType.OTHER


def capital_case(value: str) -> str:
    """Converts the value to capital case
    Parameters
    ----------
    value : str
        Value to convert to capital case"""
    new_value = ""
    if value is None:
        return new_value
    value_list = re.findall(r'[A-Z][^A-Z]*', value)
    if len(value_list) == 0:
        return value.title()
    for word in value_list:
        new_value = f"{new_value}{word.title()}"
    return new_value


