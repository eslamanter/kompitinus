import sys
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout,
                             QRadioButton, QToolButton, QFrame, QMenu, QAction)
from PyQt5.QtCore import Qt
from user_ui import UserSignup, UserLogin
from constants import APP_NAME, UI_DB_EXISTING, UI_DB_NEW, DB_NAME, UI_CONNECT, UI_SELECT_PATH, CFG_PATH
from sqlite_db import create_db
from utils import select_db_file_dialog, select_directory_dialog, join_paths, get_basename, get_directory
import config


class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # DB path Group
        db_path_group = QGroupBox(DB_NAME)
        db_path_group_layout = QVBoxLayout()

        db_radio_layout = QHBoxLayout()
        self.db_existing = QRadioButton(UI_DB_EXISTING)
        self.db_existing.setChecked(True)
        self.db_new = QRadioButton(UI_DB_NEW)
        db_radio_layout.addWidget(self.db_existing)
        db_radio_layout.addWidget(self.db_new)
        db_radio_layout.addStretch()
        db_path_group_layout.addLayout(db_radio_layout)

        db_path_layout = QHBoxLayout()
        self.db_path = QLineEdit()
        self.db_path.setReadOnly(True)
        self.db_menu_button = QToolButton(self)
        self.db_menu_button.setText("... ")
        self.db_menu_button.setPopupMode(QToolButton.InstantPopup)

        self.db_menu = QMenu(self)
        select_db_action = QAction(UI_SELECT_PATH, self)
        select_db_action.triggered.connect(self.select_db_path)
        self.db_menu.addAction(select_db_action)
        self.db_menu_button.setMenu(self.db_menu)

        db_path_layout.addWidget(self.db_path)
        db_path_layout.addWidget(self.db_menu_button)
        db_path_group_layout.addLayout(db_path_layout)

        db_path_group.setLayout(db_path_group_layout)
        layout.addWidget(db_path_group)

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Connect Button
        self.connect_button = QPushButton(UI_CONNECT)
        self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.connect_button.setEnabled(False)
        self.connect_button.clicked.connect(self.connect_db)
        layout.addWidget(self.connect_button)

        self.setLayout(layout)
        self.adjustSize()

        # Placeholder
        self.login_ui = None
        self.signup_ui = None

    def select_db_path(self):
        if self.db_existing.isChecked():
            file_path = select_db_file_dialog(parent=self, default_dir=get_directory(self.db_path.text()))
            if file_path:
                if get_basename(file_path) == DB_NAME:
                    self.db_path.setText(file_path)
                    self.connect_button.setEnabled(True)
        else:
            directory_path = select_directory_dialog(parent=self, default_dir=get_directory(self.db_path.text()))
            if directory_path:
                self.db_path.setText(join_paths(directory=directory_path, file_name=DB_NAME))
                self.connect_button.setEnabled(True)

    def connect_db(self):
        db_path = self.db_path.text()
        if db_path:
            config.config[CFG_PATH] = db_path

            # Create DB only if it doesn't exist
            new_db_created = create_db()

            # Close Config UI and show Authn UI
            self.accept()
            if new_db_created: # If new DB is created, signup is shown, otherwise, login is firstly shown
                self.show_signup()
            else:
                self.show_login()

    def show_login(self):
        if self.login_ui is None:
            self.login_ui = UserLogin()
        self.login_ui.exec()

    def show_signup(self):
        if self.signup_ui is None:
            self.signup_ui = UserSignup()
        self.signup_ui.exec()

    def closeEvent(self, event):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config_dialog = ConfigDialog()
    config_dialog.show()
    sys.exit(app.exec())
