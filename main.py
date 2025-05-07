import sys
from PyQt5.QtWidgets import QApplication
from config_json import check_config
from main_ui import MainWindow


def main():
    app = QApplication(sys.argv)
    check_config()
    main_ui = MainWindow()
    main_ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
