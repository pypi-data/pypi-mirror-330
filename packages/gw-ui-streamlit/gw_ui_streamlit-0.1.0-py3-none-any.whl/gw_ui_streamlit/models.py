from typing import Any

from pydantic import BaseModel, Field

from gw_ui_streamlit.constants import ButtonVariantType, ButtonLevel


class Option(BaseModel):
    Value: str = Field(alias="value", default=None)
    Function: str = Field(alias="function", default=None)
    OptionsFunction: Any = Field(alias="function_function", default=None)

class DefaultRow(BaseModel):
    Header: str = Field(alias="row_header", default=None)
    Row: str = Field(alias="row", default=None)


class BaseConfig(BaseModel):
    Code: str = Field(alias="code", default=None)
    Label: str = Field(alias="label", default=None)
    Enabled: str = Field(alias="enabled", default=None)
    OnClick: str = Field(alias="on_click", default=None)
    OnClickFunction: Any = Field(alias="on_click_function", default=None)
    OnChange: str = Field(alias="on_change", default=None)
    OnChangeFunction: Any = Field(alias="on_change_function", default=None)
    Tab: str = Field(alias="tab", default="Main")
    Default: Any = Field(default=None, alias="default")
    DefaultFunction: str = Field(default=None, alias="default_function")
    DefaultFunctionBuilt: Any = Field(default=None, alias="default_function_built")
    Extension: str = Field(default=None, alias="extension")
    Icon: str = Field(default=None, alias="icon")
    Immutable: bool = Field(default=False, alias="immutable")
    InputOptions: list[Option] = Field(default=None, alias="options")
    Key: str = Field(default=None, alias="key")
    ShortKey: str = Field(default=None, alias="short_key")
    Help: str = Field(default=None, alias="help")
    DateFormat: str = Field(default=None, alias="format")
    Cache: bool = Field(default=False, alias="cache")
    OnSelect: str = Field(default="rerun", alias="on_select")
    OnSelectFunction: Any = Field(default=None, alias="on_select_function")
    SelectionMode: str = Field(default="single-row", alias="selection_model")
    Hidden: bool = Field(default=False, alias="hidden")
    Placeholder: str = Field(default=None, alias="placeholder")
    DialogInputs: str = Field(default=None, alias="dialog_inputs")
    DialogAnchor: str = Field(default=None, alias="dialog_anchor")


class Button(BaseConfig):
    Variant: ButtonVariantType = Field(default=ButtonVariantType.secondary, alias="variant")
    Level: ButtonLevel = Field(default=ButtonLevel.application, alias="level")
    Popover: bool = Field(default=None, alias="popover")
    Type: str = Field(default="button", alias="type")


class Tab(BaseConfig):
    Type: str = Field(default="tab", alias="type")


class InputFieldsBase(BaseConfig):
    Required: bool = Field(default=False, alias="required")
    Min: int = Field(default=None, alias="min")
    Max: int = Field(default=None, alias="max")
    Order: str = Field(default=None, alias="order")
    Function: str = Field(alias="function", default=None)
    Type: str = Field(default="text_input", alias="type")
    DefaultRows: list[DefaultRow] = Field(default=[], alias="default_rows")
    Buttons: list[Button] = Field(default=[], alias="buttons")


class InputFields(InputFieldsBase):
    Image: str = Field(default=None, alias="image")
    Columns: list[InputFieldsBase] = Field(default=[], alias="columns")


class UserInterface(BaseConfig):
    Name: str = Field(alias="name")
    Description: str = Field(alias="description", default=None)
    Developer: str = Field(alias="developer", default=None)
    Concept: str = Field(alias="concept", default=None)
    Title: bool = Field(default=False, alias="title")
    Inputs: list[InputFields] = Field(default=[], alias="inputs")
    Tabs: list[Tab] = Field(default=[], alias="tabs")
    Buttons: list[Button] = Field(default=[], alias="buttons")
