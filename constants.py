
# Developer info
DEV_NAME = 'Eslam Anter'
DEV_EMAIL = 'eslam.anter@outlook.com'

# App info
APP_NAME = 'Kompitinus'
APP_VERSION = '1.0'
APP_PHASE = 'Beta'
APP_YEAR = '2025'

# ---------------------------------------- App About/Copyright/Disclaimer (ITA) ----------------------------------------
APP_ABOUT = """
Questa applicazione crea e gestisce un database locale condiviso, offrendo un'interfaccia per organizzare,
analizzare e condividere i compiti lavorativi con trasparenza, nel rispetto delle regole aziendali.
Permette di impostare priorità con scadenze flessibili, indicando i giorni mancanti o scaduti.
Gli utenti autenticati possono consultare il titolo e la scadenza dei compiti assegnati agli altri,
con la possibilità di esportare report riepilogativi dei compiti contrassegnati.<br>
Per maggiori informazioni, consultare Info > Guida.
"""

APP_DISCLAIMER = """
ESCLUSIONE DI RESPONSABILITÀ:<br>
Questo software gestisce un database aperto, esponendolo al rischio di modifiche esterne o danneggiamenti.
Si consiglia di non condividere informazioni sensibili o riservate.
Questo software è fornito senza alcuna garanzia di prestazioni, affidabilità o risultati."""

APP_COPYRIGHT = (f"© {APP_YEAR} {DEV_NAME}. Tutti i diritti riservati.<br>"
                 "È vietata la distribuzione o l'utilizzo non autorizzato.")
# ----------------------------------------------------------------------------------------------------------------------

# Company policy
WEEKENDS = [6, 7] # Saturday = 6, Sunday = 7
WORKING_HOURS = (9, 18) # 09:00 - 18:59

# Config
CFG_FILE = "config.json"
CFG_PATH = "path"
CFG_EMAIL = "email"
CFG_PIN = "pin"

# SQLite Database
DB_NAME = f"{APP_NAME.lower()}.db"

    # Users Table
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

    # Tasks Table
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

    # Report View
DB_REPORT_VIEW = "report"

# --------------------------------------------- Localized UI Strings (ITA) ---------------------------------------------

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
UI_MAX_TITLE_LEN = 160
UI_STARRED = "Contrassegnato"
UI_STARRED_TIP = "Contrassegnare per permettere agli altri di consultare il titolo e la scadenza"
UI_ARCHIVED = "Archiviato"
UI_ARCHIVED_TIP = "Archiviare per nascondere agli altri, incluso l'utente incaricato del compito"

UI_PLACEHOLDER_TITLE = f"Titolo (Max {UI_MAX_TITLE_LEN} caratteri)"
UI_PLACEHOLDER_BODY = "Descrizione"
UI_PLACEHOLDER_REPLY = "Risposta dell'utente incaricato del compito"

UI_REFERENCE = "Riferimento"
UI_REFERENCE_OPEN = "Seleziona cartella"
UI_REFERENCE_COPY = "Copia Link"
UI_REFERENCE_PASTE = "Incolla Link"
UI_REFERENCE_DELETE = "Cancella Link"

UI_DUE_AT = "Scade il"
UI_DUE_AT_TIP = "Data di scadenza prevista dal responsabile per il completamento del compito"
UI_EXPECTED_AT = "Previsto il"
UI_EXPECTED_AT_TIP = "Data di completamento prevista dall'utente incaricato del compito"
UI_DAYS = "gg"
UI_HOLIDAY = "Giorno non lavorativo!"
UI_OUTSIDE_HOURS = "Fuori orari lavorativi!"
UI_REPLY = "Risposta"
UI_DONE = "Fatto"
UI_DONE_TIP = "Segnare come completato"
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
UI_README_TITLE = "Readme ITA"

# Messages
MSG_SELECT_DIR = "Seleziona Cartella"
MSG_SELECT_FILE = "Seleziona File"

MSG_DB_UNREACHABLE = "Database irraggiungibile!"
MSG_EMAIL_EXISTS = "Utente già registrato."
MSG_EXCEL_OPENED = "Foglio Excel in uso."
MSG_LOGOUT = "Sei sicure di voler uscire?"
MSG_CLOSE = "Sei sicuro di voler chiudere?"

# ----------------------------------------------------------------------------------------------------------------------

# URLs
README_URL = f"https://raw.githubusercontent.com/eslamanter/kompitinus-ita/main/README.md"

# Errors
ERR_GUI = "GUI ERROR"
ERR_DB = "DB ERROR"

# Icons
MAIN_ICON = "icon.png"

# Color Palette
COLOR_LIGHT_GREY = (211, 211, 211)
COLOR_LIGHT_BLUE = (173, 216, 230)
COLOR_LIGHT_RED = (255, 204, 203)
COLOR_LIGHT_ORANGE = (255, 200, 130)
COLOR_LIGHT_GREEN = (144, 238, 144)
