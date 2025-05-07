import sys
from http.client import responses

from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGroupBox, QFrame,
                             QHBoxLayout)
from PyQt5.QtCore import Qt
import config
from about import APP_NAME
from constants import (UI_EMAIL, UI_PIN, UI_FIRST_NAME, UI_LAST_NAME, UI_UPDATE, UI_4_DIGITS, UI_SIGNUP, UI_LOGOUT,
                       UI_LOGIN, MSG_EMAIL_EXISTS, CFG_EMAIL, CFG_PIN, CFG_PATH, MSG_LOGOUT, MSG_CLOSE, MSG_WRONG_PIN)
from sqlite_db import email_exists, check_login, add_new_user, update_user_data
from utils import show_info_msg, write_config_to_json, show_question_msg, playsound_hand


class UserDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # User Group
        self.user_group = QGroupBox()

        self.first_name_label = QLabel(f"{UI_FIRST_NAME}:")
        self.first_name_input = QLineEdit()

        self.last_name_label = QLabel(f"{UI_LAST_NAME}:")
        self.last_name_input = QLineEdit()

        self.email_label = QLabel(f"{UI_EMAIL}:")
        self.email_input = QLineEdit()

        self.pin_label = QLabel(f"{UI_PIN}: ({UI_4_DIGITS})")
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setValidator((QIntValidator(0, 9999, self)))
        self.pin_input.setMaxLength(4)

        authn_layout = QVBoxLayout()
        authn_layout.addWidget(self.first_name_label)
        authn_layout.addWidget(self.first_name_input)
        authn_layout.addWidget(self.last_name_label)
        authn_layout.addWidget(self.last_name_input)
        authn_layout.addWidget(self.email_label)
        authn_layout.addWidget(self.email_input)
        authn_layout.addWidget(self.pin_label)
        authn_layout.addWidget(self.pin_input)

        self.user_group.setLayout(authn_layout)
        layout.addWidget(self.user_group)

        self.setLayout(layout)

    def check_min_data(self):
        if not self.first_name_input.text() or not self.last_name_input.text():
            return False

        if "@" not in self.email_input.text() or "." not in self.email_input.text() or len(self.email_input.text()) < 6:
            return False

        if len(self.pin_input.text()) != 4:
            return False

        return True


class UserSignup(UserDialog):
    def __init__(self):
        super().__init__()

        self.first_name_input.textChanged.connect(self.check_signup_button)
        self.last_name_input.textChanged.connect(self.check_signup_button)
        self.email_input.textChanged.connect(self.check_signup_button)
        self.pin_input.textChanged.connect(self.check_signup_button)

        layout = self.layout()
        self.user_group.setTitle(UI_SIGNUP)

        # Add update button
        self.signup_button = QPushButton(UI_SIGNUP)
        self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.signup_button.setEnabled(False)
        self.signup_button.clicked.connect(self.user_signup)
        layout.addWidget(self.signup_button)

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Add logout button
        login_layout = QHBoxLayout()

        self.login_button = QPushButton(UI_LOGIN)
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.clicked.connect(self.user_login)
        self.login_button.setStyleSheet("QPushButton { border: none; }")

        login_layout.addStretch()
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()
        layout.addLayout(login_layout)

        self.setLayout(layout)
        self.adjustSize()

        # Placeholder
        self.main_ui = None
        self.login_ui = None

    def user_signup(self):
        if email_exists(self.email_input.text()):
            show_info_msg(text=MSG_EMAIL_EXISTS)
            config.config[CFG_EMAIL] = self.email_input.text()
        else:
            add_new_user(first_name=self.first_name_input.text(),
                         last_name=self.last_name_input.text(),
                         email=self.email_input.text(),
                         pin=self.pin_input.text())

            config.config[CFG_EMAIL] = self.email_input.text()
            config.config[CFG_PIN] = self.pin_input.text()
            write_config_to_json()

        self.user_login()

    def check_signup_button(self):
        if self.check_min_data():
            self.signup_button.setEnabled(True)
        else:
            self.signup_button.setEnabled(False)

    def user_login(self):
        self.accept()
        if self.login_ui is None:
            self.login_ui = UserLogin()
        self.login_ui.exec()

    def closeEvent(self, event):
        sys.exit()


class UserUpdate(UserDialog):
    def __init__(self):
        super().__init__()

        layout = self.layout()
        self.user_group.setTitle(UI_UPDATE)

        # Add update button
        self.update_button = QPushButton(UI_UPDATE)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.clicked.connect(self.user_update)
        layout.addWidget(self.update_button)

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Add logout button
        logout_layout =QHBoxLayout()

        self.logout_button = QPushButton(UI_LOGOUT)
        self.logout_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_button.clicked.connect(self.user_logout)
        self.logout_button.setStyleSheet("QPushButton { border: none; }")

        logout_layout.addStretch()
        logout_layout.addWidget(self.logout_button)
        logout_layout.addStretch()
        layout.addLayout(logout_layout)

        self.setLayout(layout)
        self.adjustSize()

    def user_update(self):
        if self.email_input.text() == config.config[CFG_EMAIL] or not email_exists(self.email_input):
            update_user_data(first_name=self.first_name_input.text(),
                             last_name=self.last_name_input.text(),
                             email=self.email_input.text(),
                             pin=self.pin_input.text())

            config.config[CFG_EMAIL] = self.email_input.text()
            config.config[CFG_PIN] = self.pin_input.text()
            write_config_to_json()
        else:
            show_info_msg(text=MSG_EMAIL_EXISTS)

    def check_update_button(self):
        if self.check_min_data():
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)

    def user_logout(self):
        response = show_question_msg(text=MSG_LOGOUT)
        if response:
            config.config[CFG_PATH] = ""
            config.config[CFG_EMAIL] = ""
            config.config[CFG_PIN] = ""
            write_config_to_json()
            self.accept()
            sys.exit()


class UserLogin(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # Login Group
        authn_group = QGroupBox(UI_LOGIN)

        self.email_label = QLabel(f"{UI_EMAIL}:")
        self.email_input = QLineEdit(config.config[CFG_EMAIL])
        self.email_input.textChanged.connect(self.check_login_button)

        self.pin_label = QLabel(f"{UI_PIN}:")
        self.pin_input = QLineEdit(config.config[CFG_PIN])
        self.pin_input.textChanged.connect(self.check_login_button)
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setValidator((QIntValidator(0, 9999, self)))
        self.pin_input.setMaxLength(4)

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
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.user_login)
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
        self.signup_button.clicked.connect(self.user_signup)

        signup_layout.addStretch()
        signup_layout.addWidget(self.signup_button)
        signup_layout.addStretch()

        layout.addLayout(signup_layout)

        self.setLayout(layout)
        self.adjustSize()

        # Placeholder
        self.signup_ui = None

        self.check_login_button()

    def user_login(self):
        if email_exists(email=self.email_input.text()):
            if check_login(email=self.email_input.text(), pin=self.pin_input.text()):
                self.accept()

    def user_signup(self):
        self.accept()
        if self.signup_ui is None:
            self.signup_ui = UserSignup()
        self.signup_ui.exec()

    def check_min_data(self):
        if "@" not in self.email_input.text() or "." not in self.email_input.text() or len(self.email_input.text()) < 6:
            return False

        if len(self.pin_input.text()) != 4:
            return False

        return True

    def check_login_button(self):
        if self.check_min_data():
            self.login_button.setEnabled(True)
            self.user_login()
        else:
            self.login_button.setEnabled(False)

    def closeEvent(self, event):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_signup = UserSignup()
    user_update = UserUpdate()
    user_login = UserLogin()
    user_signup.show()
    # user_update.show()
    # user_login.show()
    sys.exit(app.exec())
