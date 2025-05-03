import sys
import config
from utils import file_exists, get_basename, read_config_from_json, question_msg_box
from config_ui import show_config_ui
from constants import MAIN, LOCAL, CONFIG_FILE, DB_MAIN_NAME, DB_LOCAL_NAME, MSG_DB_MAIN_NOT_FOUND


# Check if config file exists, load it & validate it, if not, create it
def check_config():
    if file_exists(CONFIG_FILE):
        path = read_config_from_json()
        if validate(path):
            config.path = path
        else:
            reset_config()
    else:
        reset_config()


def validate(path):
    if MAIN not in path or LOCAL not in path:
        return False
    if get_basename(path[MAIN]) == DB_MAIN_NAME:
        if not file_exists(path[MAIN]):
            response = question_msg_box(question=MSG_DB_MAIN_NOT_FOUND)
            if not response:
                sys.exit()
    else:
        return False
    if get_basename(path[LOCAL]) == DB_LOCAL_NAME:
        if not file_exists(path[LOCAL]):
            return False
    else:
        return False
    return True


def reset_config():
    show_config_ui()


if __name__ == "__main__":
    check_config()
    print(config.path)
