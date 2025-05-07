import json
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from about import DEV_EMAIL, APP_NAME, APP_VERSION
from constants import MSG_SELECT_DIR, MSG_SELECT_FILE, CFG_FILE
import winsound
import config


def read_config_from_json():
    with open(CFG_FILE, "r") as file:
        return json.load(file)


def write_config_to_json():
    with open(CFG_FILE, "w") as file:
        json.dump(config.db_path, file, indent=0)


def exists(path):
    return os.path.exists(path)


def send_email(email=DEV_EMAIL, title=f"{APP_NAME}_{APP_VERSION}"):
    mailto_link = f"mailto:{email}?subject=[{title}] "
    QDesktopServices.openUrl(QUrl(mailto_link))


def question_msg_box(text, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg_box.exec_()
    return result == QMessageBox.Yes


def info_msg_box(text, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def warning_msg_box(text, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

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
