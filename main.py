import sys
import config
from PyQt5.QtWidgets import QApplication
from constants import DB_NAME, CFG_FILE, CFG_PATH, CFG_EMAIL, CFG_PIN, MSG_DB_INACCESSIBLE
from sqlite_db import check_login, email_exists
from utils import exists, get_basename, read_config, show_warning_msg, valid_pin
from config_ui import ConfigDialog
from user_ui import UserLogin, UserSignup
from main_ui import MainWindow


def main():
    try:
        app = QApplication(sys.argv)
        check_config()
        main_ui = MainWindow()
        main_ui.show()
        sys.exit(app.exec())
    except Exception as e:
        show_warning_msg(e)


def check_config():
    # Check if json config file exists
    if exists(CFG_FILE):
        # Read json config file data
        json_data = read_config()
        # Check if config file contains DB path
        if CFG_PATH in json_data:
            # Check if DB name is correct
            if get_basename(json_data[CFG_PATH]) == DB_NAME:
                # Check if config file contains DB path
                if exists(json_data[CFG_PATH]):
                    # Store DB path
                    config.config[CFG_PATH] = json_data[CFG_PATH]
                    # Check if config file contains user email and pin
                    if CFG_EMAIL in json_data and CFG_PIN in json_data:
                        # Check if user email exists in DB
                        if email_exists(json_data[CFG_EMAIL]):
                            # Store user email
                            config.config[CFG_EMAIL] = json_data[CFG_EMAIL]
                            # Check if user pin is valid
                            if valid_pin(json_data[CFG_PIN]):
                                # Check login
                                if check_login(json_data[CFG_EMAIL], json_data[CFG_PIN]):
                                    # Store user pin
                                    config.config[CFG_PIN] = json_data[CFG_PIN]
                                else: # If autologin fails
                                    show_login_ui()
                            else: # If pin is not valid
                                show_login_ui()
                        else: # If email doesn't exist in DB
                            show_login_ui()
                    else: # If user email or user pin or both are missing in config.json
                        show_login_ui()
                else: # If DB file is inaccessible
                    show_warning_msg(text=MSG_DB_INACCESSIBLE)
                    sys.exit()
            else: # If DB name is wrong
                show_config_ui()
        else: # If path is missing in config.json
            show_config_ui()
    else: # If config.json is not found
        show_config_ui()


def show_main_ui():
    main_ui = MainWindow()
    main_ui.show()


def show_login_ui():
    login_ui = UserLogin()
    login_ui.exec()


def show_signup_ui():
    signup_ui = UserSignup()
    signup_ui.exec()


def show_config_ui():
    config_ui = ConfigDialog()
    config_ui.exec()


if __name__ == "__main__":
    main()
