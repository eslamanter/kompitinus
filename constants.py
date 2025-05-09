# Developer info
DEV_NAME = 'Eslam Anter'
DEV_EMAIL = 'eslam.anter@outlook.com'

# App info
APP_NAME = 'Kompitinus'
APP_VERSION = '1.0'
APP_PHASE = 'Alpha'
APP_YEAR = '2025'
APP_ABOUT = "Un'applicazione per gestire, scambiare e analizzare i compiti di lavoro."
APP_COPYRIGHT = (f"© {APP_YEAR} {DEV_NAME}. Tutti i diritti riservati.\n"
                 "È vietata la distribuzione o l'utilizzo non autorizzato.")
APP_DISCLAIMER = (f"ESCLUSIONE DI RESPONSABILITÀ:\n"
                  "Questo software è distribuito senza alcuna garanzia di prestazioni o risultati.")

# Config
CFG_FILE = "config.json"

CFG_PATH = "path"
CFG_EMAIL = "email"
CFG_PIN = "pin"

# Database
DB_NAME = f"{APP_NAME.lower()}.db"

    # Users
DB_USERS_TABLE = "users"
DB_USER_ID = "user_id"
DB_FIRST_NAME = "first_name"
DB_LAST_NAME = "last_name"
DB_EMAIL = "email"
DB_PIN = "pin"
DB_SYNC_AT = "sync_at"
DB_REGISTERED_AT = "registered_at"
DB_ACTIVE = "active"
DB_USERS_ID_BASE = 100

    # Tasks
DB_TASKS_TABLE = "tasks"
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
DB_TASKS_ID_BASE = 100000

# UI Text
    # Menubar
UI_CONFIG = "Config"
UI_DATABASE = "Database"
UI_USER = "User"
UI_LOGOUT = "Logout"
UI_SYNC_MODE = "Sync"
UI_MANUAL = "Manual"
UI_1MIN = "1 min"
UI_5MIN = "5 min"
UI_10MIN = "10 min"
UI_15MIN = "15 min"
UI_30MIN = "30 min"
UI_60MIN = "60 min"
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
UI_UPDATE = "Update"

    # Statusbar
UI_SELECTED = "Selected"
UI_COPIED = "Copied"
UI_PASTED = "Pasted"
UI_DELETED = "Deleted"

    # Config
UI_DB_EXISTING = "Existing"
UI_DB_NEW = "New"
UI_CONNECT = "Connect"
UI_SELECT_PATH = "Select Path"

    # Authn
UI_EMAIL = "Email"
UI_PIN = "Pin"
UI_LOGIN = "Login"
UI_REGISTERED = "Registered user"
UI_SIGNUP = "Sign Up"
UI_NEW_USER = "New user"

    # User
UI_USER_DATA = "User Data"
UI_FIRST_NAME = "First name"
UI_LAST_NAME = "Last name"
UI_4_DIGITS = "4 Digits"
UI_CONFIRM = "Confirm"

    # About
UI_CLOSE = "Close"

# Messages
MSG_SELECT_DIR = "Select Folder"
MSG_SELECT_FILE = "Select File"

MSG_DB_INACCESSIBLE = f"Inaccessible Database!"
MSG_EMAIL_EXISTS = "Email already exists!"
MSG_LOGOUT = "Are you sure you want to logout?"
MSG_CLOSE = "Are you sure you want to close?"

# Help
README_URL = f"https://raw.githubusercontent.com/eslamanter/{APP_NAME.lower()}/main/README.md"
