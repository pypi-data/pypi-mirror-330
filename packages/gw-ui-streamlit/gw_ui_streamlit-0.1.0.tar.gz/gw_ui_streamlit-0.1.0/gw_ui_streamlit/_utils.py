from gw_ui_streamlit.models import BaseConfig


def construct_function(function_name):
    """
    Constructs a function from the given function name.
    Parameters
    ----------
    function_name : str
        The name of the function to be constructed.
    Returns
    -------
        The constructed function if found, otherwise None.
    """
    if function_name is None:
        return None
    function_module = function_name.split(":")[0]
    function_function = function_name.split(":")[1]
    defined_function = getattr(
        __import__(function_module, globals(), locals(), [function_function]),
        function_function,
    )
    return defined_function


def option_function(item: BaseConfig):
    """
    Extracts the function from the given item.

    Args:
        item: An object containing InputOptions attribute, which is a list of items
              with Function attribute.

    Returns:
        The defined function if found, otherwise"""
    if len(item.InputOptions) == 1 and item.InputOptions[0].Function is not None:
        function_name = item.InputOptions[0].Function
        defined_function = construct_function(function_name)
        return defined_function
    else:
        return None


def built_default_original_rows(gws) -> dict:
    """
    Builds a dictionary of default rows from the YAML file.

    Args:
        gws: An object which contains yaml_file attribute.

    Returns:
        A dictionary with table labels as keys and default rows as values.
    """
    default_rows_dict = {}
    if gws.yaml_file is None:
        return default_rows_dict
    for item in [
        table_inputs
        for table_inputs in gws.yaml_file.get("inputs", [])
        if table_inputs.get("type") == "table"
    ]:
        default_rows = item.get("default_rows", dict())
        default_rows_dict[item.get("label")] = default_rows
    return default_rows_dict


def build_default_rows(gws) -> dict:
    """
    Builds a dictionary of default rows for table inputs.

    This function first constructs the default rows from the YAML file if available,
    and then updates this dictionary with the default rows from the model, if present.
    Parameters
    ----------
    gws
        An object which contains yaml_file and model attributes.

    Returns
    -------
    dict
        A dictionary with table labels as keys and default rows as values.
    """
    default_rows_dict = built_default_original_rows(gws)
    if gws.model is None:
        return default_rows_dict

    for table in [item for item in gws.model.Inputs if item.Type == "table"]:
        if table.DefaultRows is None:
            continue
        headers, rows = extract_headers_and_rows(table)
        if not headers:
            continue
        row_list = build_row_list(headers, rows)
        default_rows_dict.update({table.Label: row_list})

    return default_rows_dict


def extract_headers_and_rows(table):
    """
    Extracts headers and rows from the given table.
    Parameters
    ----------
    table
        An object containing DefaultRows attribute, which is a list of items
        with Header and Row attributes.

    Returns
    -------
    tuple
        - headers: A list of non-null headers from the table's DefaultRows.
        - rows: A list of non-null rows from the table's DefaultRows.
    """
    headers = [item.Header for item in table.DefaultRows if item.Header is not None]
    rows = [item.Row for item in table.DefaultRows if item.Row is not None]
    return headers, rows


def build_row_list(headers, rows):
    """
    Builds a list of dictionaries from the given headers and rows.
    Parameters
    ----------
    headers
        A list of headers for the table.
    rows
        A list of rows for the table.

    Returns
    -------
    list
        A list of dictionaries, each containing a header as key and row item as value.
    """
    header_list = [item.strip() for item in str(headers[0]).split(',')]
    row_list = []
    for row in rows:
        row_dict = build_row_dict(header_list, row)
        row_list.append(row_dict)
    return row_list


def build_row_dict(header_list, row):
    """
    Builds a dictionary from the given header list and row.

    Args:
        header_list: A list of headers for the table.
        row: A row item for the table.

    Returns:
        A dictionary containing headers as keys and row items as values.
    """
    row_dict = {}
    rows_items = [item.strip() for item in str(row).split(',')]
    for header in header_list:
        row_dict[header] = rows_items[header_list.index(header)]
    return row_dict
