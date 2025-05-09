from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import sys
from constants import APP_NAME, APP_VERSION, APP_PHASE, APP_ABOUT, APP_DISCLAIMER, APP_COPYRIGHT, DEV_EMAIL, UI_CLOSE
from utils import send_email


class AboutScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Info')
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)

        title_label = QLabel(f'\n{APP_NAME.upper()}\nV.{APP_VERSION} {APP_PHASE}\n', self)
        title_label.setAlignment(Qt.AlignCenter)

        body_label = QLabel(f'\n{APP_ABOUT}\n\n{APP_DISCLAIMER}\n\n{APP_COPYRIGHT}\n', self)
        body_label.setWordWrap(True)

        email_label = QLabel(f'<a href="#">{DEV_EMAIL}</a>')
        email_label.linkActivated.connect(lambda: send_email())

        close_button = QPushButton(UI_CLOSE)
        close_button.setStyleSheet("QPushButton { border: none; }")
        close_button.setCursor(QCursor(Qt.PointingHandCursor))
        close_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(body_label)
        layout.addWidget(email_label)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.adjustSize()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash_screen = AboutScreen()
    splash_screen.show()
    sys.exit(app.exec_())
