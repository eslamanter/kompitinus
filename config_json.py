import sys
from PyQt5.QtWidgets import QApplication
import config
from sqlite_db import check_login, email_exists
from utils import exists, get_basename, read_config_from_json, show_warning_msg
from config_ui import ConfigDialog
from constants import DB_NAME, CFG_FILE, CFG_PATH, CFG_EMAIL, CFG_PIN, MSG_CFG_INVALID, MSG_DB_NOT_FOUND, MSG_DB_INVALID
from user_ui import UserLogin, UserSignup


# Check if config file exists, load it & validate it, if not, reset it
def check_config():
    if exists(CFG_FILE):
        json_data = read_config_from_json()
        if validate(json_data):
            config.config = json_data
            if email_exists(email=config.config[CFG_EMAIL]):
                if check_login(email=config.config[CFG_EMAIL], pin=config.config[CFG_PIN]):
                    pass
                else:
                    show_login_ui()
            show_signup_ui()
    else:
        reset_config()


def validate(json_data):
    config_attrs = [CFG_PATH, CFG_EMAIL, CFG_PIN]
    for attr in config_attrs:
        if attr not in json_data:
            show_warning_msg(text=MSG_CFG_INVALID)
            sys.exit()

    if get_basename(json_data[CFG_PATH]) == DB_NAME:
        if not exists(json_data[CFG_PATH]):
            show_warning_msg(text=MSG_DB_NOT_FOUND)
            sys.exit()
    else:
        show_warning_msg(text=MSG_DB_INVALID)
        sys.exit()

    return True


def show_login_ui():
    login_ui = UserLogin()
    login_ui.exec()

def show_signup_ui():
    signup_ui = UserSignup()
    signup_ui.exec()

def reset_config():
    config_ui = ConfigDialog()
    config_ui.exec()


if __name__ == "__main__":
    check_config()
