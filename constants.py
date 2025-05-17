
# Developer info
DEV_NAME = 'Eslam Anter'
DEV_EMAIL = 'eslam.anter@outlook.com'

# App info
APP_NAME = 'Kompitinus'
APP_VERSION = '1.0'
APP_PHASE = 'Beta'
APP_YEAR = '2025'

# ---------- App About/Copyright/Disclaimer (Italian) ----------
APP_ABOUT = "Un'applicazione per gestire, scambiare e analizzare i compiti di lavoro."
APP_COPYRIGHT = (f"© {APP_YEAR} {DEV_NAME}. Tutti i diritti riservati.\n"
                 "È vietata la distribuzione o l'utilizzo non autorizzato.")
APP_DISCLAIMER = (f"ESCLUSIONE DI RESPONSABILITÀ:\n"
                  "Questo software è distribuito senza alcuna garanzia di prestazioni o risultati.")

# Config
CFG_FILE = "config.json"
    # Json Config File
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
DB_SEEN_AT = "seen_at"
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
DB_DONE = "done"
DB_EXPECTED_AT = "expected_at"
DB_REPLY = "reply"
DB_ARCHIVED = "archived"
DB_TASKS_ID_BASE = 100000
    # Report
DB_REPORT_VIEW = "report"

# ---------- UI Text (Italian) ----------
    # Menubar
        # User Menu
UI_USER_MENU = "Utente"
UI_USER_DATA = "Dati Utente"
        # Export
UI_EXPORT_MENU = "Esporta"
        # Info
UI_INFO_MENU = "Info"
UI_ABOUT = "App"
UI_HELP = "Guida"

    # Treeview
UI_INBOX = "Inbox"
UI_OUTBOX = "Outbox"
UI_STARRED_BOX = "Contrassegnati"
UI_EXPIRED_BOX = "Scaduti"
UI_ALL_USERS = "Utenti"
UI_SEND_TASK = "Invia un compito"

    # Tableview
UI_NOTES = "Note"
UI_EXPIRED = "Scaduto"

    # Task details panel
UI_TASK_ID = "ID"
UI_CREATED_AT = "Creato il"
UI_MODIFIED_AT = "Modificato il"
UI_SENDER = "Da"
UI_RECEIVER = "A"
UI_SEND_EMAIL_TO = "Invia una mail a"
UI_TASK = "Compito"
UI_STARRED = "Contrassegnato"
UI_STARRED_TIP = "Contrassegnato Tip"
UI_ARCHIVED = "Archiviato"
UI_ARCHIVED_TIP = "Archiviato Tip"

UI_PLACEHOLDER_TITLE = "Titolo (Max 160 Caratteri)"
UI_PLACEHOLDER_BODY = "Descrizione"
UI_PLACEHOLDER_REPLY = "Risposta"

UI_REFERENCE = "Riferimento"
UI_REFERENCE_OPEN = "Seleziona cartella"
UI_REFERENCE_COPY = "Copia Link"
UI_REFERENCE_PASTE = "Incolla Link"
UI_REFERENCE_DELETE = "Cancella Link"

UI_DUE_AT = "Scade il"
UI_EXPECTED_AT = "Previsto il"
UI_DAYS = "gg"
UI_REPLY = "Risposta"
UI_DONE = "Fatto"
UI_DONE_TIP = "Fatto Tip"
UI_SEND = "Invia"
UI_DELAY = "Ritardo"

    # Statusbar
UI_SELECTED = "Selezionato"
UI_COPIED = "Copiato"
UI_PASTED = "Incollato"
UI_DELETED = "Cancellato"
UI_TASK_SENT = "inviato con successo."
UI_TASK_UPDATED = "aggiornato con successo."

    # DB Path UI
UI_DB_EXISTING = "Esistente"
UI_DB_NEW = "Nuovo"
UI_SELECT_PATH = "Scegli percorso"
UI_CONNECT = "Connetti"

    # Login UI
UI_EMAIL = "Email"
UI_PIN = "PIN"
UI_LOGIN = "Accedi"
UI_REGISTERED = "Utente Registrato"
UI_SIGNUP = "Registrati"
UI_NEW_USER = "Nuovo Utente"

    # Sign Up UI
UI_FIRST_NAME = "Nome"
UI_LAST_NAME = "Cognome"
UI_COMPANY = "Aziendale"
UI_4_DIGITS = "4 Cifre"

    # Update User UI
UI_UPDATE = "Aggiorna"
UI_LOGOUT = "Esci"

    # About
UI_CLOSE = "Chiudi"

# Messages
MSG_SELECT_DIR = "Seleziona Cartella"
MSG_SELECT_FILE = "Seleziona File"

MSG_DB_INACCESSIBLE = f"Database inaccessibile!"
MSG_EMAIL_EXISTS = "Utente già registrato."
MSG_EXCEL_OPENED = "Foglio Excel in uso."
MSG_LOGOUT = "Sei sicure di voler uscire?"
MSG_CLOSE = "Sei sicuro di voler chiudere?"

# Help
README_URL = f"https://raw.githubusercontent.com/eslamanter/{APP_NAME.lower()}/main/README.md"
