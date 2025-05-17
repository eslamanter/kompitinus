import json
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QDateTime, QTime
from constants import DEV_EMAIL, APP_NAME, APP_VERSION, MSG_SELECT_DIR, MSG_SELECT_FILE, CFG_FILE
import winsound
import config


def count_days(deadline):
    now = QDateTime.currentDateTime()
    deadline = QDateTime.fromString(deadline, "yyyy-MM-dd HH:mm:ss")
    return now.daysTo(deadline)


def next_working_midday():
    tomorrow_date = QDateTime.currentDateTime().addDays(1)
    tomorrow_date.setTime(QTime(12, 0, 0))
    return tomorrow_date


def read_config():
    with open(CFG_FILE, "r") as file:
        return json.load(file)


def write_config():
    with open(CFG_FILE, "w") as file:
        json.dump(config.config, file, indent=0)


def exists(path):
    return os.path.exists(path)


def send_email(email=DEV_EMAIL, title=f"{APP_NAME} {APP_VERSION}"):
    mailto_link = f"mailto:{email}?subject=[{title}] "
    QDesktopServices.openUrl(QUrl(mailto_link))


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

def get_basename(file_path):
    return os.path.basename(file_path)


def get_directory(file_path):
    return os.path.dirname(file_path)


def select_directory_dialog(parent=None, title=MSG_SELECT_DIR, default_dir=""):
    directory_path = QFileDialog.getExistingDirectory(parent, title, default_dir)
    return directory_path


def select_db_file_dialog(parent=None, title=MSG_SELECT_FILE, default_dir=""):
    file_path, _ = QFileDialog.getOpenFileName(parent, title, default_dir, "Database Files (*.db)")
    return file_path


def join_paths(directory, file_name):
    return os.path.normpath(os.path.join(directory, file_name))


def playsound_hand():
    winsound.MessageBeep(winsound.MB_ICONHAND)


def playsound_exclamation():
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)


def playsound_ok():
    winsound.MessageBeep(winsound.MB_OK)


def valid_email(email):
    if "@" not in email or "." not in email or len(email) < 6:
        return False
    return True


def valid_pin(pin):
    if not pin.isdigit() or len(pin) != 4:
        return False
    return True
