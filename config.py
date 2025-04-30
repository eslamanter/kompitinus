from constants import (DB_MAIN_PATH, DB_LOCAL_PATH, DB_EMPLOYEE_ID, DB_EMPLOYEE_ID_BASE,
                       DB_FIRST_NAME, DB_LAST_NAME, DB_EMAIL, DB_PIN)
from about import APP_NAME


# Default config data
config_data = {
    DB_MAIN_PATH: f"{APP_NAME}_main.db",
    DB_LOCAL_PATH: f"{APP_NAME}_local.db",
    DB_EMPLOYEE_ID: DB_EMPLOYEE_ID_BASE,
    DB_FIRST_NAME: "",
    DB_LAST_NAME: "",
    DB_EMAIL: "",
    DB_PIN: "0000"
}
