import sys
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QGroupBox, QHBoxLayout, QRadioButton, QToolButton, QFrame, QMenu, QAction)
from PyQt5.QtCore import Qt
from about import APP_NAME
from constants import (UI_DB_EXISTING, UI_DB_NEW, DB_MAIN_NAME, DB_LOCAL_NAME,
                       UI_CONNECT, DB_LOCAL_DEFAULT_DIR, UI_SELECT_PATH, MSG_SELECT_FILE,
                       MAIN, LOCAL, MSG_SELECT_DIR, UI_EMAIL, UI_LOGIN, UI_SIGNUP, UI_PIN)
from sqlite_db import create_main_db, create_local_db
from utils import (select_db_file_dialog, select_directory_dialog, join_paths, get_basename, get_directory,
                   file_exists, playsound_hand, write_config_to_json, playsound_ok)
import config


class AuthnDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # Authn Group
        authn_group = QGroupBox()

        self.email_label = QLabel(f"{UI_EMAIL}:")
        self.email_input = QLineEdit()

        self.pin_label = QLabel(f"{UI_PIN}:")
        self.pin_input = QLineEdit()

        authn_layout = QVBoxLayout()
        authn_layout.addWidget(self.email_label)
        authn_layout.addWidget(self.email_input)
        authn_layout.addWidget(self.pin_label)
        authn_layout.addWidget(self.pin_input)

        authn_group.setLayout(authn_layout)
        layout.addWidget(authn_group)

        # Login Button
        self.login_button = QPushButton(UI_LOGIN)
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Sign up Button
        signup_layout = QHBoxLayout()

        self.signup_button = QPushButton(UI_SIGNUP)
        self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.signup_button.setStyleSheet("QPushButton { border: none; }")
        self.signup_button.clicked.connect(self.signup)

        signup_layout.addStretch()
        signup_layout.addWidget(self.signup_button)
        signup_layout.addStretch()

        layout.addLayout(signup_layout)

        self.setLayout(layout)
        self.adjustSize()

    def login(self):
        self.accept()

    def signup(self):
        self.accept()


def show_authn_ui():
    playsound_ok()
    authn_dialog = AuthnDialog()
    authn_dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    authn_dialog_ = AuthnDialog()
    authn_dialog_.show()
    sys.exit(app.exec())