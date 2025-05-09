import sqlite3
import bcrypt
import config
from utils import exists
from constants import (DB_USERS_ID_BASE, DB_USERS_TABLE, DB_USER_ID,
                       DB_FIRST_NAME, DB_LAST_NAME, DB_EMAIL, DB_PIN, DB_REGISTERED_AT, DB_ACTIVE, DB_TASKS_ID_BASE,
                       DB_TASKS_TABLE, DB_TASK_ID, DB_SENDER_ID, DB_RECEIVER_ID, DB_CREATED_AT, DB_MODIFIED_AT,
                       DB_TITLE, DB_BODY, DB_REFERENCE, DB_DUE_AT, DB_STARRED, DB_STATUS, DB_EXPECTED_AT, DB_REPLY,
                       DB_ARCHIVED, CFG_PATH, DB_SYNC_AT)


def email_exists(email):
    # Connect to DB
    conn = sqlite3.connect(config.config[CFG_PATH])
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(F"SELECT 1 FROM {DB_USERS_TABLE} WHERE {DB_EMAIL} = ?", (email,))
    result = cursor.fetchone() is not None

    # Close the connection
    conn.close()

    return result


def add_new_user(first_name, last_name, email, pin):
    # Connect to DB
    conn = sqlite3.connect(config.config[CFG_PATH])
    cursor = conn.cursor()

    # Hash user pin
    salt = bcrypt.gensalt()
    hashed_pin = bcrypt.hashpw(pin.encode(), salt)

    # User data to insert
    user_data = (first_name, last_name, email, hashed_pin,)

    # Insert query
    cursor.execute(f"""
        INSERT INTO {DB_USERS_TABLE} ({DB_FIRST_NAME}, {DB_LAST_NAME}, {DB_EMAIL}, {DB_PIN})
        VALUES (?, ?, ?, ?)
    """, user_data)

    # Get user ID
    config.my_id = cursor.lastrowid

    # Commit and close
    conn.commit()
    conn.close()


def update_user_data(first_name, last_name, email, pin):
    # Connect to DB
    conn = sqlite3.connect(config.config[CFG_PATH])
    cursor = conn.cursor()

    # Hash user pin
    salt = bcrypt.gensalt()
    hashed_pin = bcrypt.hashpw(pin.encode(), salt)

    # Update query
    cursor.execute(f"""
        UPDATE {DB_USERS_TABLE}
        SET {DB_FIRST_NAME} = ?, {DB_LAST_NAME} = ?, {DB_EMAIL} = ?, {DB_PIN} = ?
        WHERE {DB_USER_ID} = ?
    """, (first_name, last_name, email, hashed_pin, config.my_id))

    # Commit and close
    conn.commit()
    conn.close()


def check_login(email, pin):
    """Verifies login by checking email-based user ID and hashed PIN."""

    if exists(config.config[CFG_PATH]):  # Ensure database exists
        try:
            # Connect to main DB
            conn = sqlite3.connect(config.config[CFG_PATH])
            cursor = conn.cursor()

            # Retrieve user ID and hashed PIN from registered email
            cursor.execute(f"SELECT {DB_USER_ID}, {DB_PIN} FROM {DB_USERS_TABLE} WHERE {DB_EMAIL} = ?",
                           (email,))
            result = cursor.fetchone()

            if result:
                user_id, hashed_pin = result  # Extract user ID and hashed PIN
                raw = pin.encode('utf-8')  # Convert input PIN to bytes

                # Securely check hashed PIN
                if bcrypt.checkpw(raw, hashed_pin):

                    config.my_id = user_id
                    return True  # Successful login

                return False  # Incorrect PIN

            return None  # Invalid email (not registered)

        except sqlite3.Error as e:
            return None

    return None  # Database file inaccessible or doesn't exist


def create_db():
    # Ensure creating new main DB only if directory exists not in case of lost connection with local server
    if not exists(config.config[CFG_PATH]):

        # Create and connect to SQLite database
        conn = sqlite3.connect(config.config[CFG_PATH])
        cursor = conn.cursor()

        # Create users table
        cursor.execute(f"""
        CREATE TABLE {DB_USERS_TABLE} (
            {DB_USER_ID}    INTEGER UNIQUE,
            {DB_FIRST_NAME}     TEXT NOT NULL,
            {DB_LAST_NAME}      TEXT NOT NULL,
            {DB_EMAIL}          TEXT NOT NULL UNIQUE,
            {DB_PIN}            BLOB NOT NULL,
            {DB_SYNC_AT}        TEXT DEFAULT (datetime('now', 'localtime')),
            {DB_REGISTERED_AT}  TEXT DEFAULT (datetime('now', 'localtime')),
            {DB_ACTIVE}         INTEGER DEFAULT 1,
            PRIMARY KEY({DB_USER_ID} AUTOINCREMENT)
        );
        """)

        # Create tasks table
        cursor.execute(f"""
        CREATE TABLE {DB_TASKS_TABLE} (
            {DB_TASK_ID}		INTEGER UNIQUE,
            {DB_SENDER_ID}		INTEGER NOT NULL,
            {DB_RECEIVER_ID}	INTEGER NOT NULL,
            {DB_CREATED_AT}	    TEXT DEFAULT (datetime('now', 'localtime')),
            {DB_MODIFIED_AT}	TEXT DEFAULT (datetime('now', 'localtime')),
            {DB_TITLE}			TEXT,
            {DB_BODY}			TEXT,
            {DB_REFERENCE}		TEXT,
            {DB_DUE_AT}		    TEXT,
            {DB_STARRED}		INTEGER DEFAULT 0,
            {DB_STATUS}		    INTEGER,
            {DB_EXPECTED_AT}	TEXT,
            {DB_REPLY}			TEXT,
            {DB_ARCHIVED}		INTEGER DEFAULT 0,
            PRIMARY KEY({DB_TASK_ID} AUTOINCREMENT),
            FOREIGN KEY({DB_SENDER_ID}) REFERENCES {DB_USERS_TABLE}({DB_USER_ID}),
            FOREIGN KEY({DB_RECEIVER_ID}) REFERENCES {DB_USERS_TABLE}({DB_USER_ID})
        );
        """)

        # Update sqlite_sequence
        dummy_text = "dummy_text"
        dummy_int = DB_USERS_ID_BASE

        cursor.execute(
            f"INSERT INTO {DB_USERS_TABLE} ({DB_FIRST_NAME}, {DB_LAST_NAME}, {DB_EMAIL}, {DB_PIN}) VALUES ('{dummy_text}', '{dummy_text}', '{dummy_text}', '{dummy_text}')")
        cursor.execute(f"DELETE FROM {DB_USERS_TABLE} WHERE {DB_EMAIL} = '{dummy_text}'")

        cursor.execute(
            f"INSERT INTO {DB_TASKS_TABLE} ({DB_SENDER_ID}, {DB_RECEIVER_ID}, {DB_TITLE}) VALUES ({dummy_int}, {dummy_int}, '{dummy_text}')")
        cursor.execute(f"DELETE FROM {DB_TASKS_TABLE} WHERE {DB_TITLE} = '{dummy_text}'")

        cursor.execute(f"UPDATE sqlite_sequence SET seq = {DB_USERS_ID_BASE} WHERE name = '{DB_USERS_TABLE}'")
        cursor.execute(f"UPDATE sqlite_sequence SET seq = {DB_TASKS_ID_BASE} WHERE name = '{DB_TASKS_TABLE}'")

        # Commit changes and close connection
        conn.commit()
        conn.close()

        return True
    return False


if __name__ == "__main__":
    create_db()