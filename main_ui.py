import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QTableView, QSplitter, QLineEdit,
    QTextEdit, QCheckBox, QPushButton, QDateTimeEdit, QTreeView, QStatusBar, QMenu, QAction, QToolButton, QFileDialog)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtCore import Qt
from readme_ui import ReadmeViewer
from about_ui import AboutScreen
from constants import *
from about import APP_NAME
from utils import send_email, select_directory_dialog, get_directory
import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)

        central_widget = QWidget()

        # Add tree view
        self.tree_view = QTreeView(self)
        self.tree_model = QStandardItemModel()
        self.tree_view.setModel(self.tree_model)
        # self.tree_view.setHeaderHidden(True)

        # Add items to the tree view
        root_item = self.tree_model.invisibleRootItem()
        inbox_item = QStandardItem(UI_INBOX)
        outbox_item = QStandardItem(UI_OUTBOX)
        selfbox_item = QStandardItem(UI_SELFBOX)
        starred_item = QStandardItem(UI_STARRED)
        archived_item = QStandardItem(UI_ARCHIVED)

        root_item.appendRow(inbox_item)
        root_item.appendRow(outbox_item)
        root_item.appendRow(selfbox_item)
        root_item.appendRow(starred_item)
        root_item.appendRow(archived_item)

        # Create table view
        self.table_view = QTableView()

        # Create a splitter and add both tree view and table view
        self.left_splitter = QSplitter(Qt.Horizontal)
        self.left_splitter.addWidget(self.tree_view)
        self.left_splitter.addWidget(self.table_view)
        self.left_splitter.setStretchFactor(0, 1)
        self.left_splitter.setStretchFactor(1, 2)

        # Left column: Task ID, Created At, Modified At
        left_meta_layout = QVBoxLayout()
        self.task_id_label = QLabel(f"{UI_TASK_ID}:")
        self.task_id_value = QLabel("12345")
        self.created_at_label = QLabel(f"{UI_CREATED_AT}:")
        self.created_at_value = QLabel("2025-04-27 12:00")
        self.modified_at_label = QLabel(f"{UI_MODIFIED_AT}:")
        self.modified_at_value = QLabel("2025-04-27 12:30")
        left_meta_layout.addWidget(self.task_id_label)
        left_meta_layout.addWidget(self.task_id_value)
        left_meta_layout.addWidget(self.created_at_label)
        left_meta_layout.addWidget(self.created_at_value)
        left_meta_layout.addWidget(self.modified_at_label)
        left_meta_layout.addWidget(self.modified_at_value)

        # Right column: Sender, Receiver
        right_meta_layout = QVBoxLayout()
        self.sender_label = QLabel(f"{UI_SENDER}:")
        self.sender_full_name = QLabel("John Doe")
        self.sender_email = QLabel(F'<a href="#">{"example@abc.xyz"}</a>')
        self.sender_email.linkActivated.connect(lambda: send_email(email="", title=f"{APP_NAME}_{UI_TASK}_{100000}")) #

        self.receiver_label = QLabel(f"{UI_RECEIVER}:")
        self.receiver_full_name = QLabel("Jane Doe")
        self.receiver_email = QLabel(f'<a href="#">{"example@abc.xyz"}</a>')
        self.receiver_email.linkActivated.connect(lambda: send_email(email="", title=f"{APP_NAME}_{UI_TASK}_{100000}")) #

        right_meta_layout.addWidget(self.sender_label)
        right_meta_layout.addWidget(self.sender_full_name)
        right_meta_layout.addWidget(self.sender_email)
        right_meta_layout.addWidget(self.receiver_label)
        right_meta_layout.addWidget(self.receiver_full_name)
        right_meta_layout.addWidget(self.receiver_email)

        # Create a line to separate the two columns
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)

        # Combine left and right columns into one horizontal layout
        meta_layout = QHBoxLayout()
        meta_layout.addLayout(left_meta_layout)
        meta_layout.addWidget(vertical_line)
        meta_layout.addLayout(right_meta_layout)

        # Other components: Title, Body, Reference, Dates, etc.
        main_vertical_layout = QVBoxLayout()

        # Add horizontal line before Task
        horizontal_line_1 = QFrame()
        horizontal_line_1.setFrameShape(QFrame.HLine)
        horizontal_line_1.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addLayout(meta_layout)
        main_vertical_layout.addWidget(horizontal_line_1)

        # Task
        self.task_layout = QHBoxLayout()
        self.task_label = QLabel(f"{UI_TASK}:")
        self.starred_checkbox = QCheckBox(UI_STARRED)
        self.task_layout.addWidget(self.task_label)
        self.task_layout.addStretch()
        self.task_layout.addWidget(self.starred_checkbox)
        main_vertical_layout.addLayout(self.task_layout)

        # Task title input
        self.title_input = QLineEdit()
        main_vertical_layout.addWidget(self.title_input)

        # Task body input
        self.body_input = QTextEdit()
        main_vertical_layout.addWidget(self.body_input)

        # Reference
        reference_layout = QHBoxLayout()
        self.reference_label = QLabel(f"{UI_REFERENCE}:")
        self.reference_label.setOpenExternalLinks(True)
        self.menu_button = QToolButton(self)
        self.menu_button.setText("... ")
        self.menu_button.setPopupMode(QToolButton.InstantPopup)
        reference_layout.addWidget(self.reference_label)
        reference_layout.addWidget(self.menu_button)
        main_vertical_layout.addLayout(reference_layout)

        horizontal_line_2 = QFrame()
        horizontal_line_2.setFrameShape(QFrame.HLine)
        horizontal_line_2.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addWidget(horizontal_line_2)

        # Create menu associated to menu button
        self.menu = QMenu(self)
        open_directory_action = QAction(UI_REFERENCE_OPEN, self)
        open_directory_action.triggered.connect(self.open_directory_dialog)
        copy_link_action = QAction(UI_REFERENCE_COPY, self)
        copy_link_action.triggered.connect(self.copy_reference_link)
        paste_link_action = QAction(UI_REFERENCE_PASTE, self)
        paste_link_action.triggered.connect(self.paste_reference_link)
        delete_link_action = QAction(UI_REFERENCE_DELETE, self)
        delete_link_action.triggered.connect(self.delete_reference_link)
        self.menu.addAction(open_directory_action)
        self.menu.addAction(copy_link_action)
        self.menu.addAction(paste_link_action)
        self.menu.addAction(delete_link_action)
        self.menu_button.setMenu(self.menu)

        # Due At
        due_at_layout = QHBoxLayout()
        self.due_at_label = QLabel(f"{UI_DUE_AT}:")
        self.due_at_days = QLabel("42")
        self.due_at_days.setAlignment(Qt.AlignRight)
        due_at_layout.addWidget(self.due_at_label)
        due_at_layout.addWidget(self.due_at_days)
        self.due_at_input = QDateTimeEdit()
        self.due_at_input.setCalendarPopup(True)
        main_vertical_layout.addLayout(due_at_layout)
        main_vertical_layout.addWidget(self.due_at_input)

        # Expected At
        expected_at_layout = QHBoxLayout()
        self.expected_at_label = QLabel(f"{UI_EXPECTED_AT}:")
        self.expected_at_days = QLabel("56")
        self.expected_at_days.setAlignment(Qt.AlignRight)
        expected_at_layout.addWidget(self.expected_at_label)
        expected_at_layout.addWidget(self.expected_at_days)
        self.expected_at_input = QDateTimeEdit()
        self.expected_at_input.setCalendarPopup(True)
        main_vertical_layout.addLayout(expected_at_layout)
        main_vertical_layout.addWidget(self.expected_at_input)

        # Reply
        self.reply_layout = QHBoxLayout()
        self.reply_label = QLabel(f"{UI_REPLY}:")
        self.done_checkbox = QCheckBox(UI_DONE)
        self.reply_layout.addWidget(self.reply_label)
        self.reply_layout.addStretch()
        self.reply_layout.addWidget(self.done_checkbox)
        main_vertical_layout.addLayout(self.reply_layout)

        # Reply input
        self.reply_input = QTextEdit()
        main_vertical_layout.addWidget(self.reply_input)

        # Archived checkbox
        self.archived_layout = QHBoxLayout()
        self.archived_checkbox = QCheckBox(UI_ARCHIVED)
        self.archived_layout.addWidget(self.archived_checkbox)
        main_vertical_layout.addLayout(self.archived_layout)

        # Add horizontal line between checkboxes and update button
        horizontal_line_3 = QFrame()
        horizontal_line_3.setFrameShape(QFrame.HLine)
        horizontal_line_3.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addWidget(horizontal_line_3)

        # Add update task button
        self.update_button_layout = QHBoxLayout()
        self.update_button = QPushButton(UI_UPDATE)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button_layout.addWidget(self.update_button)
        main_vertical_layout.addLayout(self.update_button_layout)

        # Wrap everything in a QWidget for the splitter
        task_details_widget = QWidget()
        task_details_widget.setLayout(main_vertical_layout)

        # Create a splitter and add tree/table views and task details widget
        self.right_splitter = QSplitter(Qt.Horizontal)
        self.right_splitter.addWidget(self.left_splitter)
        self.right_splitter.addWidget(task_details_widget)

        # Set the splitter as the main layout
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.right_splitter)

        self.setCentralWidget(central_widget)

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.adjustSize()
        self.center()

    def open_directory_dialog(self):
        directory_path = select_directory_dialog(parent=self, default_dir=get_directory(config.path[MAIN]))
        self.reference_label.setText(f'<a href={directory_path}>{UI_REFERENCE}</a>')
        self.reference_label.setToolTip(directory_path)
        if directory_path:
            self.status_bar.showMessage(f"{UI_SELECTED}: {directory_path}")

    def copy_reference_link(self):
        copied_text = self.reference_label.toolTip()
        clipboard = QApplication.clipboard()
        clipboard.setText(copied_text)
        if copied_text:
            self.status_bar.showMessage(f"{UI_COPIED}: {copied_text}")

    def paste_reference_link(self):
        clipboard = QApplication.clipboard()
        pasted_text = clipboard.text()
        self.reference_label.setText(f'<a href={pasted_text}>{UI_REFERENCE}</a>')
        self.reference_label.setToolTip(pasted_text)
        if pasted_text:
            self.status_bar.showMessage(f"{UI_PASTED}: {pasted_text}")

    def delete_reference_link(self):
        deleted_text = self.reference_label.toolTip()
        self.reference_label.setText(F"{UI_REFERENCE}:")
        self.reference_label.setToolTip("")
        if deleted_text:
            self.status_bar.showMessage(f"{UI_DELETED}: {deleted_text}")

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # Config menu
        config_menu = menu_bar.addMenu(UI_CONFIG)

            # Database menu
        database_menu = config_menu.addMenu(UI_DATABASE)
        database_menu.addAction(UI_MAIN)
        database_menu.addAction(UI_LOCAL)

            # Profile menu
        profile_menu = config_menu.addMenu(UI_USER)
        profile_menu.addAction(UI_EDIT)
        profile_menu.addAction(UI_LOGOUT)

            # Sync menu
        sync_menu = config_menu.addMenu(UI_SYNC_MODE)
        sync_menu.addAction(UI_MANUAL)

                # Auto menu
        auto_sync = sync_menu.addMenu(UI_AUTO)
        auto_sync.addAction(UI_1MIN)
        auto_sync.addAction(UI_5MIN)
        auto_sync.addAction(UI_10MIN)
        auto_sync.addAction(UI_15MIN)
        auto_sync.addAction(UI_30MIN)
        auto_sync.addAction(UI_60MIN)
        auto_sync.addAction(UI_NEVER)

        # Task menu
        task_menu = menu_bar.addMenu(UI_TASK)
        task_menu.addAction(UI_SYNC_TASK)
        task_menu.addAction(UI_SEND_TASK)

        # Export menu
        export_menu = menu_bar.addMenu(UI_EXPORT)
        export_menu.addAction(UI_MAIN)
        export_menu.addAction(UI_LOCAL)

        # Info menu
        info_menu = menu_bar.addMenu(UI_INFO)
        about_action = QAction(UI_ABOUT, self)
        info_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about)
        help_action = QAction(UI_HELP, self)
        info_menu.addAction(help_action)
        help_action.triggered.connect(self.show_readme)

    def show_about(self):
        self.about_ui = AboutScreen()
        self.about_ui.show()

    def show_readme(self):
        self.readme_ui = ReadmeViewer()
        self.readme_ui.show()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


def show_main_ui():
    main_window = MainWindow()
    main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window_ = MainWindow()
    main_window_.show()
    sys.exit(app.exec())
