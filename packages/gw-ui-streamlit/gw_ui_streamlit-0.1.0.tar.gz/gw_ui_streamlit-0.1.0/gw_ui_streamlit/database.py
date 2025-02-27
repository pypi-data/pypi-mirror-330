import json
import gw_ui_streamlit.core as gws
from dbm import dumb
from gw_ui_streamlit.constants import LOCAL_DBM_LOCATION
from gw_ui_streamlit.utils import replace_short_key, update_session


def local_dbm_database(*, db_name: str, location:str = None) -> str:
    """Builds the location string to the DBM database
        Parameters
        ----------
        db_name : str
            Name of the DBM database
        location : str, optional
            If the DBM database is to be located not in the default location then the
            location needs to be supplied

        Returns
        -------
        str
            String of the path to the DBM database
    """
    if location is None:
        local_dbm = f"{LOCAL_DBM_LOCATION}/{db_name}"
    else:
        local_dbm = f"{location}/{db_name}"
    return local_dbm


def save_dbm_database(*, db_name: str, record_key: str):
    """Saves the inputs to the DBM database
    Parameters
    ----------
    db_name : str
        Name of the DBM database
    record_key : str
        Key of the record in the DBM database"""
    if record_key is None or db_name is None:
        return
    dbm_dict = dumb.open(local_dbm_database(db_name=db_name), "c")
    saved_state = json.dumps(gws.create_saved_state(short_key=True))
    dbm_dict[record_key] = saved_state
    dbm_dict.close()


def load_from_dbm_database(*, db_name: str, selection: str = None, record_key: str = None):
    """Loads the inputs from the DBM database and updates the session_state
    Parameters
    ----------
    db_name : str
        Name of the DBM database
    selection : str
        The selection key used to extract the key from the session_state
    record_key : str
        Key of the record in the DBM database"""
    if selection is None:
        key = record_key
    else:
        selected_value = gws.fetch_value_reset(name=selection)
        key = selected_value.split("-")[0].replace(" ", "")
    value = read_from_dbm_database(db_name=db_name, key=key)
    update_session(value, using_code=True)


def read_from_dbm_database(*, db_name: str, key: str, returns: str = "dict"):
    """Reads a record from the DBM database
    Parameters
    ----------
    db_name : str
        Name of the DBM database
    key : str
        Key of the record in the DBM database
    returns : str
        How the information is returned 'dict' or 'raw'
    Returns
    -------
    Python dict or raw DMB record"""
    dbm = dumb.open(local_dbm_database(db_name=db_name), "c")
    dbm_record = dbm.get(str(key))
    dbm.close()
    if returns == "dict":
        return_dict = dbm_record.decode().replace("NaN", "null")
        return json.loads(return_dict)
    else :
        return dbm_record


def list_from_dbm_database(*, db_name: str, key_structure: list = []) -> list:
    """Builds a list of keys from the DBM database, this can optionaly apply the values defined in key_structure
    Parameters
    ----------
    db_name : str
        Name of the DBM database
    key_structure : list
        List of keys used to augment the values in the return display string
    Returns
    -------
    list
        List of display strings for each of the records in the DBM database"""
    dbm_dict = dumb.open(local_dbm_database(db_name=db_name), "c")
    list_applications = []
    for key in dbm_dict.keys():
        value_key = key.decode()
        value_dict = json.loads(dbm_dict[key].decode("utf8"))
        display = f"{value_key}"
        for key in key_structure:
            display = display + f" - {value_dict[key]}"
        list_applications.append(display)
    dbm_dict.close()
    return list_applications


def delete_from_dbm_database(*, db_name: str, record_key: str):
    """Deletes a record from the DBM database, it sets each of the values to None and updates the session_state
    Parameters
    ----------
    db_name : str
        Name of the DBM database
    record_key : str
        Key of the record in the DBM database"""
    dbm_dict = dumb.open(local_dbm_database(db_name=db_name), "c")
    value = read_from_dbm_database(db_name=db_name, key=record_key)
    for key in value:
        value[key] = None
    update_session(value, using_code=True)
    dbm_dict.pop(record_key)
    dbm_dict.close()