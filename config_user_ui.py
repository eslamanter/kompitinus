import config
from constants import DB_EMAIL, DB_PIN, DB_FIRST_NAME, DB_LAST_NAME
from utils import write_config_to_json


def show_config_user_ui():
    config.data[DB_EMAIL] = "anter@hypro.it"
    config.data[DB_PIN] = "3310"
    config.data[DB_FIRST_NAME] = "Eslam"
    config.data[DB_LAST_NAME] = "Anter"

    write_config_to_json()
