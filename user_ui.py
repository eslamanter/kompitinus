import sys
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGroupBox, QFrame
from PyQt5.QtCore import Qt
from about import APP_NAME
from constants import (UI_EMAIL, UI_PIN, UI_FIRST_NAME, UI_LAST_NAME, UI_UPDATE, UI_USER_DATA, UI_4_DIGITS, UI_CONFIRM,
                       UI_SIGNUP)
from main_ui import MainWindow


class UserDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # User Group
        user_group = QGroupBox(UI_USER_DATA)

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

        user_group.setLayout(authn_layout)
        layout.addWidget(user_group)



        # --- SEPARATE TWO CLASSES ---
        # layout = self.layout()

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Add update/signup button
        self.update_button = QPushButton(UI_UPDATE)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.clicked.connect(self.update)
        layout.addWidget(self.update_button)

        self.setLayout(layout)
        self.adjustSize()

        # Placeholder
        self.main_ui = None

    def update(self):
        self.accept()

    def show_main_ui(self):
        if self.main_ui is None:
            self.main_ui = MainWindow()
        self.main_ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_dialog = UserDialog()
    user_dialog.show()
    sys.exit(app.exec())
