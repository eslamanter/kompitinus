import sys
import json
from PyQt5.QtWidgets import QApplication
from constants import CONFIG_FILE, DB_MAIN_PATH, MSG_CREATE_CONFIG, MSG_CREATE_DB
from main_ui import show_main_ui
from utils import check_file_exists, info_msg_box, question_msg_box, select_folder_dialog
from sqlite_db import check_sqlite_db
import config


# Check if config file exists, load it, if not, create it
def check_config_file():
    if check_file_exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config.config_data = json.load(file)
            check_sqlite_db(config.config_data[DB_MAIN_PATH])
    else:
        with open(CONFIG_FILE, "w") as file:
            app = QApplication(sys.argv)
            if not question_msg_box(MSG_CREATE_CONFIG):
                sys.exit()
            folder_path = select_folder_dialog()
            if folder_path:
                check_sqlite_db(folder_path)
            else:
                sys.exit()
            json.dump(config.config_data, file, indent=0)


if __name__ == "__main__":
    check_config_file()
    print(config.config_data)
