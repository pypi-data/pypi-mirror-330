# -*- encoding: utf-8 -*-
import sys
import json
import base64

from pyrpc_schedule.meta.key import ADMIN_USERNAME_KEY, DEFAULT_USERNAME_KEY, DEFAULT_PASSWORD_KEY, \
    ADMIN_PASSWORD_KEY, SYSTEM_DEFAULT_SCHEDULE_TIME_KEY, SYSTEM_DEFAULT_SCHEDULE_TIME, TASK_ID_KEY, \
    TASK_IS_SUB_TASK_KEY, TASK_IS_SUB_TASK_ALL_FINISH_KEY, TASK_SOURCE_ID_KEY

from pyrpc_schedule.utils.cipher.cipher import Cipher
from pyrpc_schedule.utils.network.socket_tools import SocketTools
from pyrpc_schedule.utils.format_time.format_time import FormatTime
from pyrpc_schedule.utils.generate_id.generate_id import SnowflakeID
from pyrpc_schedule.utils.logger.logger import Logger

__all__ = [
    'Cipher',
    'SocketTools',
    'FormatTime',
    'SnowflakeID',
    'Logger',
    'load_config',
    'blank_dictionary_value_processing',
    'config_default_value_processing',
    'task_required_field_check'
]


def load_config(encoded_config):
    """
    Decode and load the encoded configuration string.

    Args:
        encoded_config (str): The encoded configuration string.

    Returns:
        dict: The decoded configuration dictionary.
    """
    try:
        encoded_bytes = encoded_config.encode('utf-8')
        decoded_bytes = base64.b64decode(encoded_bytes)
        decoded_string = decoded_bytes.decode('utf-8')
        return json.loads(decoded_string)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def blank_dictionary_value_processing(data: dict, key: str, is_bool: bool = False):
    """
    Process the value of a dictionary key.
    Args:
        data (dict): The dictionary containing the key-value pair.
        key (str): The key to process.
        is_bool (bool, optional): Indicates if the value should be treated as a boolean. Defaults to False.
    Returns:
        bool: True if the key exists in the dictionary and the value is not None or an empty string.
    """

    if key in data and data[key] is not None and data[key] != '':
        if is_bool is False:
            return True

        if type(data[key]) is str and data[key].lower() == 'true':
            return True

        if type(data[key]) is bool and data[key] is True:
            return True
    return False


def config_default_value_processing(config: dict):
    """
    Process the default values in the configuration dictionary.
    Args:
        config (dict): The configuration dictionary.
    Returns:
        dict: The configuration dictionary with processed default values.
    """

    if ADMIN_USERNAME_KEY not in config:
        config[ADMIN_USERNAME_KEY] = DEFAULT_USERNAME_KEY

    if ADMIN_PASSWORD_KEY not in config:
        config[ADMIN_PASSWORD_KEY] = DEFAULT_PASSWORD_KEY

    if SYSTEM_DEFAULT_SCHEDULE_TIME_KEY not in config:
        config[SYSTEM_DEFAULT_SCHEDULE_TIME_KEY] = SYSTEM_DEFAULT_SCHEDULE_TIME

    return config


def task_required_field_check(message: dict):
    """
    Check if the required fields are present in the task message.
    Args:
        message (dict): The task message.
    Raises:
        Exception: If any of the required fields are missing.
    Returns:
        message (dict): The task message.
    """

    if blank_dictionary_value_processing(data=message, key=TASK_ID_KEY) is False:
        message[TASK_ID_KEY] = SnowflakeID().generate_id()

    if blank_dictionary_value_processing(data=message, key=TASK_IS_SUB_TASK_KEY, is_bool=True) is False:
        message[TASK_IS_SUB_TASK_KEY] = False

    if blank_dictionary_value_processing(data=message, key=TASK_IS_SUB_TASK_ALL_FINISH_KEY) is False:
        message[TASK_IS_SUB_TASK_ALL_FINISH_KEY] = False

    if blank_dictionary_value_processing(data=message, key=TASK_IS_SUB_TASK_KEY, is_bool=True):
        if blank_dictionary_value_processing(data=message, key=TASK_SOURCE_ID_KEY) is False:
            raise Exception('send_message : task source id is None')

    return message
