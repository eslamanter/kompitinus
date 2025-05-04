import sys
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGroupBox,
                             QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from about import APP_NAME
from constants import UI_EMAIL, UI_LOGIN, UI_SIGNUP, UI_PIN
from utils import playsound_hand
from user_ui import UserDialog
import bcrypt

# # Hashing a password
# password = "MySecurePassword".encode('utf-8')
# hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
#
# # Verifying a password
# if bcrypt.checkpw(password, hashed_password):
#     print("Password is correct!")


class AuthnDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # Authn Group
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

        # Placeholder
        self.user_ui = None

    def login(self):
        self.accept()

    def signup(self):
        self.accept()

    def show_user_ui(self):
        if self.user_ui is None:
            self.user_ui = UserDialog()
        self.user_ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    authn_dialog = AuthnDialog()
    authn_dialog.show()
    sys.exit(app.exec())