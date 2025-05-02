import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout,
    QGroupBox, QHBoxLayout, QRadioButton, QToolButton, QFrame, QMenu, QAction)
from PyQt5.QtCore import Qt
from about import APP_NAME
from config_user_ui import show_config_user_ui
from constants import (UI_DB_CONFIG, UI_DB_EXISTING, UI_DB_NEW, DB_MAIN_NAME, DB_LOCAL_NAME,
                       UI_CHECK, DB_LOCAL_DEFAULT_DIR, UI_SELECT_PATH, MSG_SELECT_FILE,
                       MAIN, LOCAL, MSG_SELECT_DIR, DB_MAIN_PATH, DB_LOCAL_PATH)
from utils import (select_db_file_dialog, select_directory_dialog, join_paths, get_basename, check_file_exists,
                   playsound_hand, playsound_exclamation)
import config


class DBConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - {UI_DB_CONFIG}")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        layout = QVBoxLayout()

        # Main DB Group
        main_db_group = QGroupBox(DB_MAIN_NAME)
        main_db_layout = QVBoxLayout()

        main_db_radio_layout = QHBoxLayout()
        self.main_db_existing = QRadioButton(UI_DB_EXISTING)
        self.main_db_existing.setChecked(True)
        self.main_db_new = QRadioButton(UI_DB_NEW)
        main_db_radio_layout.addWidget(self.main_db_existing)
        main_db_radio_layout.addWidget(self.main_db_new)
        main_db_radio_layout.addStretch()
        main_db_layout.addLayout(main_db_radio_layout)

        main_db_path_layout = QHBoxLayout()
        self.main_db_path = QLineEdit()
        self.main_db_path.setReadOnly(True)
        self.main_db_menu_button = QToolButton(self)
        self.main_db_menu_button.setText("... ")
        self.main_db_menu_button.setPopupMode(QToolButton.InstantPopup)

        self.main_db_menu = QMenu(self)
        select_main_db_action = QAction(UI_SELECT_PATH, self)
        select_main_db_action.triggered.connect(lambda: self.select_db_path(MAIN))
        self.main_db_menu.addAction(select_main_db_action)
        self.main_db_menu_button.setMenu(self.main_db_menu)

        main_db_path_layout.addWidget(self.main_db_path)
        main_db_path_layout.addWidget(self.main_db_menu_button)
        main_db_layout.addLayout(main_db_path_layout)

        main_db_group.setLayout(main_db_layout)
        layout.addWidget(main_db_group)

        # Local DB Group
        local_db_group = QGroupBox(DB_LOCAL_NAME)
        local_db_layout = QVBoxLayout()

        local_db_radio_layout = QHBoxLayout()
        self.local_db_existing = QRadioButton(UI_DB_EXISTING)
        self.local_db_new = QRadioButton(UI_DB_NEW)
        self.local_db_new.setChecked(True)
        local_db_radio_layout.addWidget(self.local_db_existing)
        local_db_radio_layout.addWidget(self.local_db_new)
        local_db_radio_layout.addStretch()
        local_db_layout.addLayout(local_db_radio_layout)

        local_db_path_layout = QHBoxLayout()
        self.local_db_path = QLineEdit()
        if check_file_exists(DB_LOCAL_DEFAULT_DIR):
            self.local_db_path.setText(join_paths(directory_path=DB_LOCAL_DEFAULT_DIR, file_name=DB_LOCAL_NAME))
        self.local_db_path.setReadOnly(True)
        self.local_db_menu_button = QToolButton(self)
        self.local_db_menu_button.setText("... ")
        self.local_db_menu_button.setPopupMode(QToolButton.InstantPopup)

        self.local_db_menu = QMenu(self)
        select_local_db_action = QAction(UI_SELECT_PATH, self)
        select_local_db_action.triggered.connect(lambda: self.select_db_path(LOCAL))
        self.local_db_menu.addAction(select_local_db_action)
        self.local_db_menu_button.setMenu(self.local_db_menu)

        local_db_path_layout.addWidget(self.local_db_path)
        local_db_path_layout.addWidget(self.local_db_menu_button)
        local_db_layout.addLayout(local_db_path_layout)

        local_db_group.setLayout(local_db_layout)
        layout.addWidget(local_db_group)

        # Add horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(horizontal_line)

        # Connect Button
        self.check_button = QPushButton(UI_CHECK)
        self.check_button.clicked.connect(self.check_db_config)
        layout.addWidget(self.check_button)

        self.setLayout(layout)
        self.adjustSize()

    def select_db_path(self, db):
        if db == MAIN:
            if self.main_db_existing.isChecked():
                file_path = select_db_file_dialog(parent=self, title=f"{MSG_SELECT_FILE} {DB_MAIN_NAME}")
                if file_path:
                    if get_basename(file_path) == DB_MAIN_NAME:
                        self.main_db_path.setText(file_path)
            else:
                directory_path = select_directory_dialog(parent=self, title=f"{MSG_SELECT_DIR} {DB_MAIN_NAME}")
                if directory_path:
                    self.main_db_path.setText(join_paths(directory_path=directory_path, file_name=DB_MAIN_NAME))
        else:
            if self.local_db_existing.isChecked():
                file_path = select_db_file_dialog(parent=self, title=f"{MSG_SELECT_FILE} {DB_LOCAL_NAME}")
                if file_path:
                    if get_basename(file_path) == DB_LOCAL_NAME:
                        self.local_db_path.setText(file_path)
            else:
                directory_path = select_directory_dialog(parent=self, title=f"{MSG_SELECT_DIR} {DB_LOCAL_NAME}")
                if directory_path:
                    self.local_db_path.setText(join_paths(directory_path=directory_path, file_name=DB_LOCAL_NAME))

    def check_db_config(self):
        main_db_path = self.main_db_path.text()
        local_db_path = self.local_db_path.text()
        if main_db_path and local_db_path:
            config.data[DB_MAIN_PATH] = main_db_path
            config.data[DB_LOCAL_PATH] = local_db_path
            self.accept()

            show_config_user_ui()

        else:
            playsound_hand()


def show_config_db_ui():
    playsound_exclamation()
    config_dialog = DBConfigDialog()
    config_dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config_dialog_ = DBConfigDialog()
    config_dialog_.show()
    sys.exit(app.exec())
