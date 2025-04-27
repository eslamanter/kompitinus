import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QTableView, QSplitter, QLineEdit, QTextEdit, QCheckBox,
    QPushButton, QDateTimeEdit, QTreeView, QStatusBar)
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
        starred_item = QStandardItem("Starredbox")
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
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFrameShadow(QFrame.Sunken)

        # Combine left and right columns into one horizontal layout
        meta_layout = QHBoxLayout()
        meta_layout.addLayout(left_meta_layout)
        meta_layout.addWidget(separator_line)
        meta_layout.addLayout(right_meta_layout)

        # Other components: Title, Body, Reference, Dates, etc.
        main_vertical_layout = QVBoxLayout()

        # Add horizontal line before Task
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addLayout(meta_layout)
        main_vertical_layout.addWidget(horizontal_line)

        # Task
        self.task_label = QLabel("Task:")
        self.title_input = QLineEdit()
        main_vertical_layout.addWidget(self.task_label)
        main_vertical_layout.addWidget(self.title_input)

        # Task Body
        self.body_input = QTextEdit()
        main_vertical_layout.addWidget(self.body_input)

        # Reference
        self.reference_label = QLabel("Reference:")
        self.reference_input = QLineEdit()
        main_vertical_layout.addWidget(self.reference_label)
        main_vertical_layout.addWidget(self.reference_input)

        # Due At
        due_at_layout = QVBoxLayout()
        due_at_labels_layout = QHBoxLayout()
        self.due_at_label = QLabel("Due At:")
        self.due_at_number = QLabel("42")  # Number of days
        self.due_at_number.setAlignment(Qt.AlignRight)
        due_at_labels_layout.addWidget(self.due_at_label)
        due_at_labels_layout.addWidget(self.due_at_number)
        self.due_at_input = QDateTimeEdit()
        self.due_at_input.setCalendarPopup(True)
        due_at_layout.addLayout(due_at_labels_layout)
        due_at_layout.addWidget(self.due_at_input)
        main_vertical_layout.addLayout(due_at_layout)

        # Expected At
        expected_at_layout = QVBoxLayout()
        expected_at_labels_layout = QHBoxLayout()
        self.expected_at_label = QLabel("Expected At:")
        self.expected_at_number = QLabel("56")  # Number of days
        self.expected_at_number.setAlignment(Qt.AlignRight)
        expected_at_labels_layout.addWidget(self.expected_at_label)
        expected_at_labels_layout.addWidget(self.expected_at_number)
        self.expected_at_input = QDateTimeEdit()
        self.expected_at_input.setCalendarPopup(True)
        expected_at_layout.addLayout(expected_at_labels_layout)
        expected_at_layout.addWidget(self.expected_at_input)
        main_vertical_layout.addLayout(expected_at_layout)

        # Reply
        self.reply_label = QLabel("Reply:")
        self.reply_input = QTextEdit()
        main_vertical_layout.addWidget(self.reply_label)
        main_vertical_layout.addWidget(self.reply_input)

        # Task Starred, Done, and Archived
        self.checkbox_layout = QHBoxLayout()
        self.task_starred_checkbox = QCheckBox("Task Starred")
        self.task_done_checkbox = QCheckBox("Task Done")
        self.task_archived_checkbox = QCheckBox("Archived")
        self.checkbox_layout.addWidget(self.task_starred_checkbox)
        self.checkbox_layout.addWidget(self.task_done_checkbox)
        self.checkbox_layout.addWidget(self.task_archived_checkbox)
        main_vertical_layout.addLayout(self.checkbox_layout)

        # Add horizontal line between checkboxes and update button
        separator_line_between_sections = QFrame()
        separator_line_between_sections.setFrameShape(QFrame.HLine)
        separator_line_between_sections.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addWidget(separator_line_between_sections)

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

        self.adjustSize()
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())