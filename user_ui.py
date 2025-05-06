import sys
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGroupBox, QFrame,
                             QHBoxLayout)
from PyQt5.QtCore import Qt
from about import APP_NAME
from constants import (UI_EMAIL, UI_PIN, UI_FIRST_NAME, UI_LAST_NAME, UI_UPDATE, UI_USER_DATA, UI_4_DIGITS, UI_CONFIRM,
                       UI_SIGNUP, UI_LOGOUT, UI_LOGIN)
from main_ui import MainWindow


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

        self.pin_label_1 = QLabel(f"{UI_PIN}: ({UI_4_DIGITS})")
        self.pin_input_1 = QLineEdit()
        self.pin_input_1.setEchoMode(QLineEdit.Password)
        self.pin_input_1.setValidator((QIntValidator(0, 9999, self)))
        self.pin_input_1.setMaxLength(4)

        self.pin_label_2 = QLabel(f"{UI_PIN}: ({UI_CONFIRM})")
        self.pin_input_2 = QLineEdit()
        self.pin_input_2.setEchoMode(QLineEdit.Password)
        self.pin_input_2.setValidator((QIntValidator(0, 9999, self)))
        self.pin_input_2.setMaxLength(4)

        authn_layout = QVBoxLayout()
        authn_layout.addWidget(self.first_name_label)
        authn_layout.addWidget(self.first_name_input)
        authn_layout.addWidget(self.last_name_label)
        authn_layout.addWidget(self.last_name_input)
        authn_layout.addWidget(self.email_label)
        authn_layout.addWidget(self.email_input)
        authn_layout.addWidget(self.pin_label_1)
        authn_layout.addWidget(self.pin_input_1)
        authn_layout.addWidget(self.pin_label_2)
        authn_layout.addWidget(self.pin_input_2)

        self.user_group.setLayout(authn_layout)
        layout.addWidget(self.user_group)

        self.setLayout(layout)


class UserSignup(UserDialog):
    def __init__(self):
        super().__init__()

        layout = self.layout()
        self.user_group.setTitle(UI_SIGNUP)

        # Add update button
        self.signup_button = QPushButton(UI_SIGNUP)
        self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.accept()
        self.show_main_ui()

    def show_main_ui(self):
        self.accept()
        if self.main_ui is None:
            self.main_ui = MainWindow()
        self.main_ui.show()

    def user_login(self):
        self.accept()
        if self.login_ui is None:
            self.login_ui = UserLogin()
        self.login_ui.show()


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
        self.accept()

    def user_logout(self):
        self.accept()


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
        self.email_input = QLineEdit()

        self.pin_label = QLabel(f"{UI_PIN}:")
        self.pin_input = QLineEdit()
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

    def user_login(self):


        self.accept()



    def user_signup(self):
        self.accept()
        if self.signup_ui is None:
            self.signup_ui = UserSignup()
        self.signup_ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_signup = UserSignup()
    user_update = UserUpdate()
    user_login = UserLogin()
    user_signup.show()
    # user_update.show()
    # user_login.show()
    sys.exit(app.exec())
