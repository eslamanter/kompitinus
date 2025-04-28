import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QTableView, QSplitter, QLineEdit, QTextEdit, QCheckBox,
    QPushButton, QDateTimeEdit, QTreeView, QStatusBar, QMenu, QAction, QToolButton, QFileDialog, QMenuBar)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Add tree view
        self.tree_view = QTreeView(self)
        self.tree_model = QStandardItemModel()
        self.tree_view.setModel(self.tree_model)
        # self.tree_view.setHeaderHidden(True)

        # Add items to the tree view
        root_item = self.tree_model.invisibleRootItem()
        inbox_item = QStandardItem("Inbox")
        outbox_item = QStandardItem("Outbox")
        selfbox_item = QStandardItem("Selfbox")
        starred_item = QStandardItem("Starred")
        archived_item = QStandardItem("Archive")

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
        self.task_id_label = QLabel("Task ID:")
        self.task_id_value = QLabel("12345")
        self.created_at_label = QLabel("Created At:")
        self.created_at_value = QLabel("2025-04-27 12:00")
        self.modified_at_label = QLabel("Modified At:")
        self.modified_at_value = QLabel("2025-04-27 12:30")
        left_meta_layout.addWidget(self.task_id_label)
        left_meta_layout.addWidget(self.task_id_value)
        left_meta_layout.addWidget(self.created_at_label)
        left_meta_layout.addWidget(self.created_at_value)
        left_meta_layout.addWidget(self.modified_at_label)
        left_meta_layout.addWidget(self.modified_at_value)

        # Right column: Sender, Receiver
        right_meta_layout = QVBoxLayout()
        self.sender_label = QLabel("Sender:")
        self.sender_full_name = QLabel("John Doe")
        self.sender_email = QLabel("john.doe@example.com")
        self.receiver_label = QLabel("Receiver:")
        self.receiver_full_name = QLabel("Jane Doe")
        self.receiver_email = QLabel("jane.doe@example.com")
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
        self.task_label = QLabel("Task:")
        self.starred_checkbox = QCheckBox("Starred")
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
        self.reference_label = QLabel("Reference:")
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
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        copy_link_action = QAction("Copy Link", self)
        copy_link_action.triggered.connect(self.copy_reference_link)
        paste_link_action = QAction("Paste Link", self)
        paste_link_action.triggered.connect(self.paste_reference_link)
        delete_link_action = QAction("Delete Link", self)
        delete_link_action.triggered.connect(self.delete_reference_link)
        self.menu.addAction(open_folder_action)
        self.menu.addAction(copy_link_action)
        self.menu.addAction(paste_link_action)
        self.menu.addAction(delete_link_action)
        self.menu_button.setMenu(self.menu)

        # Due At
        due_at_layout = QHBoxLayout()
        self.due_at_label = QLabel("Due at:")
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
        self.expected_at_label = QLabel("Expected at:")
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
        self.reply_label = QLabel("Reply:")
        self.done_checkbox = QCheckBox("Done")
        self.reply_layout.addWidget(self.reply_label)
        self.reply_layout.addStretch()
        self.reply_layout.addWidget(self.done_checkbox)
        main_vertical_layout.addLayout(self.reply_layout)

        # Reply input
        self.reply_input = QTextEdit()
        main_vertical_layout.addWidget(self.reply_input)

        # Archived checkbox
        self.archived_layout = QHBoxLayout()
        self.archived_checkbox = QCheckBox("Archived")
        self.archived_layout.addWidget(self.archived_checkbox)
        main_vertical_layout.addLayout(self.archived_layout)

        # Add horizontal line between checkboxes and update button
        horizontal_line_3 = QFrame()
        horizontal_line_3.setFrameShape(QFrame.HLine)
        horizontal_line_3.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addWidget(horizontal_line_3)

        # Add update task button
        self.update_button_layout = QHBoxLayout()
        self.update_button = QPushButton("Update Task")
        self.update_button_layout.addWidget(self.update_button)
        main_vertical_layout.addLayout(self.update_button_layout)

        # Wrap everything in a QWidget for the splitter
        task_details_widget = QWidget()
        task_details_widget.setLayout(main_vertical_layout)

        # Create a splitter and add the table view and task details widget
        self.right_splitter = QSplitter(Qt.Horizontal)
        self.right_splitter.addWidget(self.left_splitter)
        self.right_splitter.addWidget(task_details_widget)

        # Set the splitter as the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.right_splitter)
        self.setLayout(layout)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.reference_label.setText(f'<a href={folder_path}>Reference:</a>')
        self.reference_label.setToolTip(folder_path)

    def copy_reference_link(self):
        copied_text = self.reference_label.toolTip()
        clipboard = QApplication.clipboard()
        clipboard.setText(copied_text)

    def paste_reference_link(self):
        clipboard = QApplication.clipboard()
        pasted_text = clipboard.text()
        self.reference_label.setText(f'<a href={pasted_text}>Reference:</a>')
        self.reference_label.setToolTip(pasted_text)

    def delete_reference_link(self):
        self.reference_label.setText("Reference:")
        self.reference_label.setToolTip("")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HYtask")

        # Set main widget as the central widget
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        self.create_menu_bar()
        self.adjustSize()
        self.center()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # Profile Menu
        profile_menu = menu_bar.addMenu("Profile")
        profile_menu.addAction("Edit Profile")
        profile_menu.addAction("Logout")

        # Task Menu
        task_menu = menu_bar.addMenu("Task")
        task_menu.addAction("Update")
        task_menu.addAction("Send")



        # Info Menu
        info_menu = menu_bar.addMenu("Info")
        info_menu.addAction("About")
        info_menu.addAction("Help")

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())