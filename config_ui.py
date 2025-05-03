import sys
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout,
    QGroupBox, QHBoxLayout, QRadioButton, QToolButton, QFrame, QMenu, QAction)
from PyQt5.QtCore import Qt
from about import APP_NAME
from authn_ui import show_authn_ui
from constants import (UI_DB_EXISTING, UI_DB_NEW, DB_MAIN_NAME, DB_LOCAL_NAME,
                       UI_CONNECT, DB_LOCAL_DEFAULT_DIR, UI_SELECT_PATH, MSG_SELECT_FILE,
                       MAIN, LOCAL, MSG_SELECT_DIR)
from sqlite_db import create_main_db, create_local_db
from utils import (select_db_file_dialog, select_directory_dialog, join_paths, get_basename, get_directory,
                   file_exists, playsound_hand, playsound_exclamation, write_config_to_json)
import config


class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
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
        if file_exists(DB_LOCAL_DEFAULT_DIR):
            self.local_db_path.setText(join_paths(directory=DB_LOCAL_DEFAULT_DIR, file_name=DB_LOCAL_NAME))
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
        self.connect_button = QPushButton(UI_CONNECT)
        self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.connect_button.clicked.connect(self.check_db_config)
        layout.addWidget(self.connect_button)

        self.setLayout(layout)
        self.adjustSize()

    def select_db_path(self, db):
        if db == MAIN:
            if self.main_db_existing.isChecked():
                file_path = select_db_file_dialog(parent=self,
                                                  title=f"{MSG_SELECT_FILE} {DB_MAIN_NAME}",
                                                  default_dir=get_directory(self.main_db_path.text()))
                if file_path:
                    if get_basename(file_path) == DB_MAIN_NAME:
                        self.main_db_path.setText(file_path)
            else:
                directory_path = select_directory_dialog(parent=self,
                                                         title=f"{MSG_SELECT_DIR} {DB_MAIN_NAME}",
                                                         default_dir=get_directory(self.main_db_path.text()))
                if directory_path:
                    self.main_db_path.setText(join_paths(directory=directory_path, file_name=DB_MAIN_NAME))
        else:
            if self.local_db_existing.isChecked():
                file_path = select_db_file_dialog(parent=self,
                                                  title=f"{MSG_SELECT_FILE} {DB_LOCAL_NAME}",
                                                  default_dir=get_directory(self.local_db_path.text()))
                if file_path:
                    if get_basename(file_path) == DB_LOCAL_NAME:
                        self.local_db_path.setText(file_path)
            else:
                directory_path = select_directory_dialog(parent=self,
                                                         title=f"{MSG_SELECT_DIR} {DB_LOCAL_NAME}",
                                                         default_dir=get_directory(self.local_db_path.text()))
                if directory_path:
                    self.local_db_path.setText(join_paths(directory=directory_path, file_name=DB_LOCAL_NAME))

    def check_db_config(self):
        main_db_path = self.main_db_path.text()
        local_db_path = self.local_db_path.text()
        if main_db_path and local_db_path:
            config.path[MAIN] = main_db_path
            config.path[LOCAL] = local_db_path
            write_config_to_json()
            self.accept()

            show_authn_ui()

            create_main_db() # To delete
            create_local_db() # To delete
        else:
            playsound_hand()


def show_config_ui():
    playsound_exclamation()
    config_dialog = ConfigDialog()
    config_dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config_dialog_ = ConfigDialog()
    config_dialog_.show()
    sys.exit(app.exec())
