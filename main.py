import sys
from PyQt5.QtWidgets import QApplication
from config_json import check_config
from main_ui import show_main_ui

def main():
    app = QApplication(sys.argv)
    check_config()
    show_main_ui()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
