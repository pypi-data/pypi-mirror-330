from enum import Enum


class KeyType(Enum):
    INPUT = "input"
    BUTTON = "button"
    TAB = "tab"
    STORAGE = "storage"
    TABLE = "table"
    OTHER = "other"


class ButtonVariantType(Enum):
    primary = "primary"
    secondary = "secondary"


class ButtonLevel(Enum):
    application = "application"
    tab = "tab"
    table = "table"


DEFAULT_BUTTONS = [
    {
        "label": "Submit",
        "on_click": "gw_ui_streamlit.utils:button_submit",
        "type": "submit",
        "variant": "primary",
    },
    {
        "label": "Cancel",
        "on_click": "gw_ui_streamlit.utils:button_cancel",
        "type": "cancel",
        "variant": "secondary",
    },
]

DEFAULT_TABEL_BUTTONS = [
    {
        "label": "Add",
        "on_click": "gw_ui_streamlit.utils:button_submit",
        "type": "submit",
        "variant": "primary",
    },
    {
        "label": "Edit",
        "on_click": "gw_ui_streamlit.utils:button_cancel",
        "type": "cancel",
        "variant": "secondary",
    },
    {
        "label": "Remove",
        "on_click": "gw_ui_streamlit.utils:button_cancel",
        "type": "cancel",
        "variant": "secondary",
    },
]

YAML_UI_LOCATION = "./resources/yaml_ui"
LOCAL_DBM_LOCATION = "./resources/local_dbm"
DEFAULT_DATE_FORMAT = "YYYY-MM-DD"
