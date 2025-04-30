from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys
import config
from about import *


class AboutUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Info')
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)

        label_title = QLabel(f'\n{APP_NAME}\nV.{APP_VERSION} {APP_PHASE}\n', self)
        label_body = QLabel(f'\n{APP_ABOUT}\n\n{APP_DISCLAIMER}\n\n{APP_COPYRIGHT}\n\n{DEV_EMAIL}\n', self)

        label_body.setWordWrap(True)
        label_title.setAlignment(Qt.AlignCenter)

        v_layout = QVBoxLayout()
        v_layout.addWidget(label_title)
        v_layout.addWidget(label_body)
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