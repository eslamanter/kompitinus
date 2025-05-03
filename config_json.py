import config
from utils import file_exists, get_basename, read_config_from_json, write_config_to_json
from config_db_ui import show_config_db_ui
from constants import (CONFIG_FILE, DB_MAIN_PATH, DB_LOCAL_PATH, DB_MAIN_NAME, DB_LOCAL_NAME,
                       DB_EMPLOYEE_ID, DB_FIRST_NAME, DB_LAST_NAME, DB_EMAIL, DB_PIN)


# Check if config file exists, load it & validate it, if not, create it
def check_config():
    if file_exists(CONFIG_FILE):
        json_data = read_config_from_json()
        if validate_config_data(json_data):
            config.data = json_data
        else:
            reset_config()
    else:
        reset_config()


def validate_config_data(config_data):
    config_keys = (DB_MAIN_PATH,
                   DB_LOCAL_PATH,
                   DB_EMPLOYEE_ID,
                   DB_FIRST_NAME,
                   DB_LAST_NAME,
                   DB_EMAIL,
                   DB_PIN)
    for key in config_keys:
        if key not in config_data:
            return False
    if file_exists(config_data[DB_MAIN_PATH]):
        if get_basename(config_data[DB_MAIN_PATH]) != DB_MAIN_NAME:
            return False
    else:
        return False
    if file_exists(config_data[DB_LOCAL_PATH]):
        if get_basename(config_data[DB_LOCAL_PATH]) != DB_LOCAL_NAME:
            return False
    else:
        return False
    if not config_data[DB_EMPLOYEE_ID].isdigit():
        return False
    return True


def reset_config():
    show_config_db_ui()


if __name__ == "__main__":
    check_config()
    print(config.data)
