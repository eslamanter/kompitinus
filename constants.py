from about import APP_NAME

# Config
CONFIG_FILE = "config.json"
DB_MAIN = "main"
DB_LOCAL = "local"
DB_MAIN_PATH = "db_main_path"
DB_LOCAL_PATH = "db_local_path"

# Database
    # Employees
DB_EMPLOYEE_ID = "employee_id"
DB_FIRST_NAME = "first_name"
DB_LAST_NAME = "last_name"
DB_EMAIL = "email"
DB_PIN = "pin"
DB_REGISTERED_AT = "registered_at"
DB_ACTIVE = "active"
DB_EMPLOYEE_ID_BASE = 100

    # Tasks
DB_TASK_ID  = "task_id"
DB_SENDER_ID = "sender_id"
DB_RECEIVER_ID = "receiver_id"
DB_CREATED_AT = "created_at"
DB_MODIFIED_AT =  "modified_at"
DB_TITLE = "title"
DB_BODY = "body"
DB_REFERENCE = "reference"
DB_DUE_AT = "due_at"
DB_STARRED = "starred"
DB_STATUS = "status"
DB_EXPECTED_AT = "expected_at"
DB_REPLY = "reply"
DB_ARCHIVED = "archived"
DB_TASK_ID_BASE = 100000

# UI Text
    # Menubar
UI_CONFIG = "Config"
UI_DATABASE = "Database"
UI_MAIN = DB_MAIN.capitalize()
UI_LOCAL = DB_LOCAL.capitalize()
UI_USER = "User"
UI_EDIT = "Edit"
UI_LOGOUT = "Logout"
UI_SYNC_MODE = "Sync"
UI_MANUAL = "Manual"
UI_AUTO = "Auto"
UI_1MIN = "1 min"
UI_5MIN = "5 min"
UI_10MIN = "10 min"
UI_15MIN = "15 min"
UI_30MIN = "30 min"
UI_60MIN = "60 min"
UI_NEVER = "Never"
UI_SYNC_TASK = "Sync"
UI_SEND_TASK = "Send"
UI_EXPORT = "Export"
UI_INFO = "Info"
UI_ABOUT = "About"
UI_HELP = "Help"

    # Treeview
UI_INBOX = "Inbox"
UI_OUTBOX = "Outbox"
UI_SELFBOX = "Selfbox"
UI_STARREDBOX = "Starred"
UI_ARCHIVEDBOX = "Archive"

    # Task details panel
UI_TASK_ID = "Task ID"
UI_CREATED_AT = "Created at"
UI_MODIFIED_AT = "Modified at"
UI_SENDER = "Sender"
UI_RECEIVER = "Receiver"
UI_TASK = "Task"
UI_STARRED = "Starred"

UI_REFERENCE = "Reference"
UI_REFERENCE_OPEN = "Browse Folder"
UI_REFERENCE_COPY = "Copy Link"
UI_REFERENCE_PASTE = "Paste Link"
UI_REFERENCE_DELETE = "Delete Link"

UI_DUE_AT = "Due at"
UI_EXPECTED_AT = "Expected at"
UI_DAYS = "Days"
UI_REPLY = "Reply"
UI_DONE = "Done"
UI_ARCHIVED = "Archive"
UI_UPDATE_TASK = "Update Task"

    # Statusbar
UI_SELECTED = "Selected"
UI_COPIED = "Copied"
UI_PASTED = "Pasted"
UI_DELETED = "Deleted"

# Messages
MSG_SELECT_FOLDER = "Select Folder"
MSG_SELECT_FILE = "Select File"
MSG_CREATE_CONFIG = "User config not found. Do you want to create new config?"
MSG_CREATE_DB = "Database not found. Do you want to create new database?"

# Readme
README_URL = f"https://raw.githubusercontent.com/eslamanter/{APP_NAME.lower()}/main/README.md"
