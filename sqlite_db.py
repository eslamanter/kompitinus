import sqlite3
import os
import config
from constants import *

def main_db_conncet():
    if os.path.exists(config.db_path[DB_MAIN_PATH]):
        conn = sqlite3.connect(config.db_path[DB_MAIN_PATH])
        cursor = conn.cursor()
        print("Connected to the existing database successfully!")

        cursor.execute("SELECT * FROM employees;")
        print(cursor.fetchall())

        conn.close()
    else:
        print("Error: Database does not exist!")


if __name__ == "__main__":
    main_db_conncet()
