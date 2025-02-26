"""
    This module is used to get environment variables.
    In case the environment variable is not set, it will return the default value.
"""

import os


def get_str(key: str, default: str = "") -> str:
    """_summary_

    Args:
        key (str): env key
        default (str, optional): Defaults to "".

    Returns:
        str: _description_
    """
    val = os.getenv(key)
    if val is None:
        val = default
    return val


def get_bool(key: str, default: bool = False) -> bool:
    """_summary_

    Args:
        key (str): env key
        default (bool, optional): Defaults to "".

    Returns:
        bool: True or False based on bool(env)
    """
    val = os.getenv(key)
    if val is None:
        return default
    if val.upper() == "FALSE" or val == 0:
        return False

    if val.upper() == "TRUE" or val == 1:
        return True
    return default


def get_int(key: str, default: int = 0) -> int:
    """_summary_

    Args:
        key (str): _description_
        default (int, optional): _description_. Defaults to 0.

    Returns:
        int: _description_
    """
    val = os.getenv(key)
    if val is None:
        return default
    return int(val)


def get_float(key: str, default: float = 0.) -> float:
    """_summary_

    Args:
        key (str): _description_
        default (float, optional): _description_. Defaults to 0..

    Returns:
        float: _description_
    """
    val = os.getenv(key)
    if val is None:
        return default
    return float(val)


def get_set(key: str, default: set = ()) -> set:
    """_summary_

    Args:
        key (str): _description_
        default (set, optional): _description_. Defaults to ().

    Returns:
        set: _description_
    """
    val = os.getenv(key)
    if val is None:
        return default
    return set(val.split(","))


def get_list(key: str, default: list = None) -> list:
    """_summary_

    Args:
        key (str): _description_
        default (list, optional): _description_. Defaults to None.

    Returns:
        list: _description_
    """
    if default is None:
        default = []
    val = os.getenv(key)
    if val is None:
        return default
    return list(val.split(","))



def det_str(dict: dict) -> str:
    """_summary_

    Args:
        dict (dict): _description_

    Returns:
        dict: _description_
    """
    value = get_str(dict["key"], dict["default"])
    return value