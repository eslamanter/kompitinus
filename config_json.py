import sys
import json
from PyQt5.QtWidgets import QApplication
from constants import (CONFIG_FILE, DB_MAIN_PATH, DB_LOCAL_PATH, DB_MAIN_NAME, DB_LOCAL_NAME,
                       MSG_NEW_CONFIG, MSG_INVALID_CONFIG, MSG_EXISTS_DB_MAIN, MSG_NEW_DB_MAIN,
                       MSG_EXISTS_DB_LOCAL, MSG_NEW_DB_LOCAL, MSG_SELECT_DIR, MSG_SELECT_FILE, DB_LOCAL_DEFAULT_DIR)
from utils import (check_file_exists, question_msg_box, warning_msg_box, select_folder_dialog, join_paths,
                   select_db_file_dialog)
from sqlite_db import check_sqlite_db, create_db_main, create_db_local
from user_ui import user_function
import config


# Check if config file exists, load it, if not, create it
def check_config_file():
    if check_file_exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            json_data = json.load(file)

        if check_config_data(json_data):
            config.config_data = json_data
            check_sqlite_db()
        else:
            warning_msg_box(MSG_INVALID_CONFIG) #
            sys.exit() #

    else:
        app = QApplication(sys.argv)
        if question_msg_box(MSG_NEW_CONFIG):

            if question_msg_box(MSG_EXISTS_DB_MAIN):
                file_path = select_db_file_dialog(title=f"{MSG_SELECT_FILE} {DB_MAIN_NAME}")
                if file_path:
                    config.config_data[DB_MAIN_PATH] = file_path
                else:
                    sys.exit()
            else:
                if question_msg_box(MSG_NEW_DB_MAIN):
                    folder_path = select_folder_dialog(title=f"{MSG_SELECT_DIR} {DB_MAIN_NAME}")
                    config.config_data[DB_MAIN_PATH] = join_paths(folder_path, DB_MAIN_NAME)
                    create_db_main()
                else:
                    sys.exit()

            if question_msg_box(MSG_EXISTS_DB_LOCAL):
                file_path = select_db_file_dialog(title=f"{MSG_SELECT_FILE} {DB_LOCAL_NAME}")
                if file_path:
                    config.config_data[DB_LOCAL_PATH] = file_path
                else:
                    sys.exit()
            else:
                if question_msg_box(MSG_NEW_DB_LOCAL):
                    folder_path = select_folder_dialog(title=f"{MSG_SELECT_DIR} {DB_LOCAL_NAME}",
                                                       default_path=DB_LOCAL_DEFAULT_DIR)
                    config.config_data[DB_LOCAL_PATH] = join_paths(folder_path, DB_LOCAL_NAME)
                    create_db_local()
                else:
                    sys.exit()

            user_function()
        else:
            sys.exit()

        with open(CONFIG_FILE, "w") as file:
            json.dump(config.config_data, file, indent=0)


def check_config_data(data):
    return True


if __name__ == "__main__":
    check_config_file()
    print(config.config_data)
