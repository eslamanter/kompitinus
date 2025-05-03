import sys
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGroupBox, QFrame
from PyQt5.QtCore import Qt
from about import APP_NAME
from constants import UI_EMAIL, UI_PIN, UI_FIRST_NAME, UI_LAST_NAME, UI_UPDATE


class UserDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # User Group
        user_group = QGroupBox()

        self.email_label = QLabel(f"{UI_EMAIL}:")
        self.email_input = QLineEdit()

        self.pin_label = QLabel(f"{UI_PIN}:")
        self.pin_input = QLineEdit()
        self.pin_input.setValidator((QIntValidator(0,9999, self)))
        self.pin_input.setMaxLength(4)

        self.first_name_label = QLabel(f"{UI_FIRST_NAME}:")
        self.first_name_input = QLineEdit()

        self.last_name_label = QLabel(f"{UI_LAST_NAME}:")
        self.last_name_input = QLineEdit()

        authn_layout = QVBoxLayout()
        authn_layout.addWidget(self.email_label)
        authn_layout.addWidget(self.email_input)
        authn_layout.addWidget(self.pin_label)
        authn_layout.addWidget(self.pin_input)
        authn_layout.addWidget(self.first_name_label)
        authn_layout.addWidget(self.first_name_input)
        authn_layout.addWidget(self.last_name_label)
        authn_layout.addWidget(self.last_name_input)

        user_group.setLayout(authn_layout)
        layout.addWidget(user_group)

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Update Button
        self.login_button = QPushButton(UI_UPDATE)
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.clicked.connect(self.update)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.adjustSize()

    def update(self):
        self.accept()


def show_user_ui():
    user_dialog = UserDialog()
    user_dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_dialog_ = UserDialog()
    user_dialog_.show()
    sys.exit(app.exec())
