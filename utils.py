import json
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QDateTime, QTime
from constants import DEV_EMAIL, APP_NAME, APP_VERSION, MSG_SELECT_DIR, MSG_SELECT_FILE, CFG_FILE
import winsound
import config


def count_days(deadline):
    """Counts days from now to a given deadline."""
    now = QDateTime.currentDateTime()
    deadline = QDateTime.fromString(deadline, "yyyy-MM-dd HH:mm:ss")
    return now.daysTo(deadline)


def next_working_midday():
    """Retrieves formatted date-time of tomorrow's midday."""
    tomorrow_date = QDateTime.currentDateTime().addDays(1)
    tomorrow_date.setTime(QTime(12, 0, 0))
    return tomorrow_date


def read_config():
    """Retrieves local config data from json file."""
    with open(CFG_FILE, "r") as file:
        return json.load(file)


def write_config():
    """Writes config data into json file."""
    with open(CFG_FILE, "w") as file:
        json.dump(config.config, file, indent=0)


def exists(path):
    """Checks if a given file or directory path exists."""
    return os.path.exists(path)


def send_email(email=DEV_EMAIL, title=f"{APP_NAME} {APP_VERSION}"):
    """Sends email optionally to given address and title or by default to app dev address."""
    mailto_link = f"mailto:{email}?subject=[{title}] "
    QDesktopServices.openUrl(QUrl(mailto_link))


def get_basename(file_path):
    """Retrieves file name from a given full path."""
    return os.path.basename(file_path)


def get_directory(file_path):
    """Retrieves file directory excluding its name from a given full path."""
    return os.path.dirname(file_path)


def select_directory_dialog(parent=None, title=MSG_SELECT_DIR, default_dir=""):
    """Opens a select folder dialog given optionally parent class, title, and default directory."""
    directory_path = QFileDialog.getExistingDirectory(parent, title, default_dir)
    return directory_path


def select_db_file_dialog(parent=None, title=MSG_SELECT_FILE, default_dir=""):
    """Opens a select .db file dialog given optionally parent class, title, and default directory."""
    file_path, _ = QFileDialog.getOpenFileName(parent, title, default_dir, "Database Files (*.db)")
    return file_path


def join_paths(directory, file_name):
    """Joins directory and file into os-valid and py-recognizable path."""
    return os.path.normpath(os.path.join(directory, file_name))



def valid_email(email):
    """Checks if a given email address is valid."""
    if "@" not in email or "." not in email or len(email) < 6:
        return False
    return True


def valid_pin(pin):
    """Checks if a given user pin is valid."""
    if not pin.isdigit() or len(pin) != 4:
        return False
    return True


def playsound_hand():
    winsound.MessageBeep(winsound.MB_ICONHAND)


def playsound_ok():
    winsound.MessageBeep(winsound.MB_OK)


def show_question_msg(text, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg_box.exec()
    return result == QMessageBox.Yes


def show_info_msg(text, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


def show_warning_msg(text, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()
