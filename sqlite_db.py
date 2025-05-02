import sqlite3
import config
from utils import check_file_exists
from constants import DB_MAIN_PATH

# def main_db_conncet():
#     if os.path.exists(config.db_path[DB_MAIN_PATH]):
#         conn = sqlite3.connect(config.db_path[DB_MAIN_PATH])
#         cursor = conn.cursor()
#         print("Connected to the existing database successfully!")
#
#         cursor.execute("SELECT * FROM employees;")
#         print(cursor.fetchall())
#
#         conn.close()
#     else:
#         print("Error: Database does not exist!")


def check_sqlite_db():
    if check_file_exists(config.config_data[DB_MAIN_PATH]):
        pass


def connect_db_main():
    pass


def create_db_main():
    pass


def create_db_local():
    pass


#
# if __name__ == "__main__":
#     main_db_conncet()
