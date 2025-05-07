import sys
from PyQt5.QtWidgets import QApplication
import config
from utils import exists, get_basename, read_config_from_json, warning_msg_box
from config_ui import ConfigDialog
from constants import DB_NAME, CFG_FILE, CFG_PATH, CFG_ID, CFG_PIN, MSG_CFG_INVALID, MSG_DB_NOT_FOUND, MSG_DB_INVALID
from main_ui import MainWindow


# Check if config file exists, load it & validate it, if not, reset it
def check_config():
    if exists(CFG_FILE):
        json_data = read_config_from_json()
        if validate(json_data):
            config.config = json_data
    else:
        reset_config()


def validate(json_data):
    config_attrs = [CFG_PATH, CFG_ID, CFG_PIN]
    for attr in config_attrs:
        if attr not in json_data:
            warning_msg_box(text=MSG_CFG_INVALID)
            sys.exit()

    if get_basename(json_data[CFG_PATH]) == DB_NAME:
        if not exists(json_data[CFG_PATH]):
            warning_msg_box(text=MSG_DB_NOT_FOUND)
            sys.exit()
    else:
        warning_msg_box(text=MSG_DB_INVALID)
        sys.exit()

    return True


def reset_config():
    config_ui = ConfigDialog()
    config_ui.exec()


if __name__ == "__main__":
    check_config()
