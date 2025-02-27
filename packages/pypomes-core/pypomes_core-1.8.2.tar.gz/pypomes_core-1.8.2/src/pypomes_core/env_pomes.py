import os
from contextlib import suppress
from datetime import date
from dateutil import parser
from dateutil.parser import ParserError
from pathlib import Path
from typing import Final

# the prefix for the names of the environment variables
APP_PREFIX: Final[str] = os.getenv("PYPOMES_APP_PREFIX", "")


def env_get_str(key: str,
                values: list[str] = None,
                def_value: str = None) -> str:
    """
    Retrieve and return the string value defined for *key* in the current operating environment.

    If *values* is specified, the value obtained is checked for occurrence therein.

    :param key: the key the value is associated with
    :param values: optional list of valid values
    :param def_value: the default value to return, if the key has not been defined
    :return: the string value associated with the key
    """
    result: str | None = os.getenv(key)
    if result is None:
        result = def_value
    elif values and result not in values:
        result = None

    return result


def env_get_int(key: str,
                values: list[int] = None,
                def_value: int = None) -> int:
    """
    Retrieve and return the integer value defined for *key* in the current operating environment.

    If *values* is specified, the value obtained is checked for occurrence therein.

    :param key: the key the value is associated with
    :param values: optional list of valid values
    :param def_value: the default value to return, if the key has not been defined
    :return: the integer value associated with the key
    """
    result: int | None
    try:
        result = int(os.environ[key])
        if values and result not in values:
            result = None
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_float(key: str,
                  values: list[float] = None,
                  def_value: float = None) -> float:
    """
    Retrieve and return the float value defined for *key* in the current operating environment.

    If *values* is specified, the value obtained is checked for occurrence therein.

    :param key: the key the value is associated with
    :param values: optional list of valid values
    :param def_value: the default value to return, if the key has not been defined
    :return: the float value associated with the key
    """
    result: float | None
    try:
        result = float(os.environ[key])
        if values and result not in values:
            result = None
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_strs(key: str,
                 values: list[str] = None) -> list[str]:
    """
    Retrieve and return the string values defined for *key* in the current operating environment.

    The values must be provided as a comma-separated list of strings.
    If *values* is specified, the values obtained are checked for occurrence therein.
    On failure, 'None' is returned.

    :param key: the key the values ares associated with
    :param values: optional list of valid values
    :return: the string values associated with the key
    """
    result: list[str] | None = None
    vals: str = os.getenv(key)
    if vals:
        result = vals.split(",")
        if values:
            for val in result:
                if val not in values:
                    result = None
                    break
    return result


def env_get_ints(key: str,
                 values: list[str] = None) -> list[int]:
    """
    Retrieve and return the integer values defined for *key* in the current operating environment.

    The values must be provided as a comma-separated list of integers.
    If *values* is specified, the values obtained are checked for occurrence therein.
    On failure, 'None' is returned.

    :param key: the key the values ares associated with
    :param values: optional list of valid values
    :return: the integer values associated with the key
    """
    result: list[int] | None = None
    # noinspection PyUnusedLocal
    with suppress(Exception):
        vals: list[str] = os.environ[key].split(",")
        if vals:
            result = [int(val) for val in vals]
            if values:
                for val in result:
                    if val not in values:
                        result = None
                        break
    return result


def env_get_floats(key: str,
                   values: list[str] = None) -> list[float]:
    """
    Retrieve and return the float values defined for *key* in the current operating environment.

    The values must be provided as a comma-separated list of floats.
    If *values* is specified, the values obtained are checked for occurrence therein.
    On failure, 'None' is returned.

    :param key: the key the values ares associated with
    :param values: optional list of valid values
    :return: the float values associated with the key
    """
    result: list[float] | None = None
    # noinspection PyUnusedLocal
    with suppress(Exception):
        vals: list[str] = os.environ[key].split(",")
        if vals:
            result = [float(val) for val in vals]
            if values:
                for val in result:
                    if val not in values:
                        result = None
                        break
    return result


def env_get_bytes(key: str,
                  values: list[bytes] = None,
                  def_value: bytes = None) -> bytes:
    """
    Retrieve and return the byte value defined for *key* in the current operating environment.

    The corresponding string defined in the environment must be a hexadecimal representation
    of the byte value. As such, it is restricted to contain characters in the range *[0-9a-f]*.
    If *values* is specified, the value obtained is checked for occurrence therein.

    :param key: the key the value is associated with
    :param values: optional list of valid values
    :param def_value: the default value to return, if the key has not been defined
    :return: the byte value associated with the key
    """
    result: bytes | None
    try:
        result = bytes.fromhex(os.environ[key])
        if values and result not in values:
            result = None
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_bool(key: str,
                 def_value: bool = None) -> bool:
    """
    Retrieve and return the boolean value defined for *key* in the current operating environment.

    These are the criteria:
        - case is disregarded
        - the string values accepted to stand for *True* are *1*, *t*, or *true*
        - the string values accepted to stand for *False* are *0*, *f*, or *false*
        - all other values causes *None* to be returned

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the boolean value associated with the key, or 'None' if a boolean value could not be established
    """
    result: bool | None
    try:
        if os.environ[key].lower() in ["1", "t", "true"]:
            result = True
        elif os.environ[key].lower() in ["0", "f", "false"]:
            result = False
        else:
            result = None
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_date(key: str,
                 def_value: date = None) -> date:
    """
    Retrieve and return the date value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the date value associated with the key
    """
    result: date
    try:
        result = parser.parse(os.environ[key]).date()
    except (AttributeError, KeyError, TypeError, ParserError, OverflowError):
        result = def_value

    return result


def env_get_path(key: str,
                 def_value: Path = None) -> Path:
    """
    Retrieve and return the path value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the path value associated with the key
    """
    result: Path
    try:
        result = Path(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_is_docker() -> bool:
    """
    Determine whether the application is running inside a Docker container.

    Note that a resonable, but not infallible, heuristics is used.

    :return: 'True' if this could be determined, 'False' otherwise
    """
    result: bool = os.path.exists('/.dockerenv')
    if not result:
        with suppress(Exception):
            with open('/proc/1/cgroup', 'rt') as f:
                result = "docker" in f.read()

    return result
