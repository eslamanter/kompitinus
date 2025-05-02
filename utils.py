import os
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from about import DEV_EMAIL, APP_NAME, APP_VERSION
from constants import MSG_SELECT_DIR, MSG_SELECT_FILE


def check_file_exists(file_path):
    return os.path.exists(file_path)


def send_email(email=DEV_EMAIL, title=f"{APP_NAME}_{APP_VERSION}"):
    mailto_link = f"mailto:{email}?subject=[{title}] "
    QDesktopServices.openUrl(QUrl(mailto_link))


def question_msg_box(question, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setText(question)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg_box.exec_()
    return result == QMessageBox.Yes


def info_msg_box(info, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(info)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def warning_msg_box(warning, title=APP_NAME):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setText(warning)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

def select_folder_dialog(parent=None, title=MSG_SELECT_DIR, default_path=""):
    folder_path = QFileDialog.getExistingDirectory(parent, title, default_path)
    return folder_path


def select_db_file_dialog(parent=None, title=MSG_SELECT_FILE, default_path=""):
    file_path, _ = QFileDialog.getOpenFileName(parent, title, default_path, "Database Files (*.db)")
    return file_path


def join_paths(folder_path, file_name):
    os.path.join(folder_path, file_name)


# def get_documents_path():
#     return join_paths(folder_path=os.path.expanduser("~"), file_name="Documents")
