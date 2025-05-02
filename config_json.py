import sys
import json
from config_db_ui import show_config_db_ui
from constants import (CONFIG_FILE, DB_MAIN_PATH, DB_LOCAL_PATH, DB_MAIN_NAME, DB_LOCAL_NAME,
                       DB_EMPLOYEE_ID, DB_FIRST_NAME, DB_LAST_NAME, DB_EMAIL, DB_PIN)
from config_user_ui import show_config_user_ui
from utils import check_file_exists, get_basename
import config


# Check if config file exists, load it, if not, create it
def check_config():
    if check_file_exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            json_data = json.load(file)
        if check_config_data(json_data):
            config.config_data = json_data
        else:
            reset_config()
    else:
        show_config_db_ui()
        with open(CONFIG_FILE, "w") as file:
            json.dump(config.config_data, file, indent=0)


def check_config_data(config_data):
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
    if get_basename(config_data[DB_MAIN_PATH]) != DB_MAIN_NAME:
        return False
    if get_basename(config_data[DB_LOCAL_PATH]) != DB_LOCAL_NAME:
        return False
    if not config_data[DB_EMPLOYEE_ID].isdigit():
        return False
    return True


def reset_config():
    show_config_db_ui()
    show_config_user_ui()


if __name__ == "__main__":
    check_config()
    print(config.config_data)
