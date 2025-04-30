from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QUrl
import sys
from about import APP_NAME, APP_VERSION, APP_PHASE, APP_ABOUT, APP_DISCLAIMER, APP_COPYRIGHT, DEV_EMAIL
from utils import send_email


class AboutUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Info')
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)

        title_label = QLabel(f'\n{APP_NAME.upper()}\nV.{APP_VERSION} {APP_PHASE}\n', self)
        body_label = QLabel(f'\n{APP_ABOUT}\n\n{APP_DISCLAIMER}\n\n{APP_COPYRIGHT}\n', self)
        email_label = QLabel(f'<a href="#">{DEV_EMAIL}</a>')
        email_label.linkActivated.connect(lambda: send_email())

        body_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignCenter)

        v_layout = QVBoxLayout()
        v_layout.addWidget(title_label)
        v_layout.addWidget(body_label)
        v_layout.addWidget(email_label)
        self.setLayout(v_layout)

        self.adjustSize()
        self.center()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = AboutUI()
    splash.show()
    sys.exit(app.exec_())