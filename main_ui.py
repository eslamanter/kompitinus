import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QTableView, QSplitter, QLineEdit,
    QTextEdit, QCheckBox, QPushButton, QDateTimeEdit, QTreeView, QStatusBar, QMenu, QAction, QToolButton,
    QHeaderView, QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor, QBrush, QColor
from PyQt5.QtCore import Qt, QDateTime
from readme_ui import ReadmeViewer
from about_ui import AboutScreen
from constants import *
from sqlite_db import get_all_users, add_task, update_task, get_tasks, get_task_details, get_user_full_name, \
    get_user_email
from user_ui import UserUpdate
from utils import send_email, select_directory_dialog, get_directory, show_question_msg, next_working_midday
import config


class TaskTableModel(QStandardItemModel):
    def __init__(self, tasks, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels([UI_TASK_ID, UI_MODIFIED_AT, UI_SENDER, UI_RECEIVER, UI_TASK, UI_DUE_AT, UI_NOTES])

        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        for task in tasks:
            (task_id, modified_at, starred, archived, title, due_at, done,
             sender_first_name, sender_last_name, receiver_first_name, receiver_last_name) = task
            sender_full_name = f"{sender_first_name}\n{sender_last_name}"
            receiver_full_name = f"{receiver_first_name}\n{receiver_last_name}"

            task_id_item = QStandardItem(str(task_id))
            task_id_item.setData(task_id, Qt.UserRole)

            modified_at_item = QStandardItem(modified_at.replace(" ", "\n"))
            sender_full_name_item = QStandardItem(sender_full_name)
            receiver_full_name_item = QStandardItem(receiver_full_name)
            title_item = QStandardItem(title)
            due_at_item = QStandardItem(due_at.replace(" ", "\n"))

            expired = True if current_time > due_at else False

            notes = ""
            if done or archived:
                notes += f"- {UI_DONE}\n" if done else ""
                notes += f"- {UI_ARCHIVED}\n" if archived else ""
            else:
                notes += f"- {UI_STARRED}\n" if starred else ""
                notes += f"- {UI_EXPIRED}\n" if expired else ""

            notes_item = QStandardItem(notes.strip())

            for item in ([task_id_item, modified_at_item, sender_full_name_item, receiver_full_name_item,
                            title_item, due_at_item, notes_item]):
                if archived:
                    item.setBackground((QBrush(QColor(211, 211, 211))))  # Light grey
                elif done:
                    item.setBackground((QBrush(QColor(173, 216, 230))))  # Light blue
                elif expired:
                    if starred:
                        item.setBackground((QBrush(QColor(255, 204, 203))))  # Light red
                    else:
                        item.setBackground((QBrush(QColor(255, 200, 130))))  # Light orange
                else:
                    item.setBackground((QBrush(QColor(144, 238, 144))))  # Light green

                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Disable editing

            self.appendRow([task_id_item, modified_at_item, sender_full_name_item, receiver_full_name_item,
                            title_item, due_at_item, notes_item])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)

        central_widget = QWidget()

        self.tree_view = QTreeView(self)
        self.tree_model = QStandardItemModel()
        self.tree_view.setModel(self.tree_model)
        self.tree_view.header().setHidden(True)

        # Define custom item roles for the treeview
        self.BOX_ROLE = Qt.UserRole
        self.FILTER_ROLE = Qt.UserRole + 1
        self.USER_ROLE = Qt.UserRole + 2

        def create_sub_items(name):
            item = QStandardItem(name)
            item.setData(name, self.FILTER_ROLE)
            return item

        # Create Parent Items
        my_boxes_items = QStandardItem(config.config[CFG_EMAIL])
        all_users_items = QStandardItem(UI_ALL_USERS)

        # Create child items for my_boxes_items
        inbox_item = QStandardItem(UI_INBOX)
        outbox_item = QStandardItem(UI_OUTBOX)

        inbox_item.setData(UI_INBOX, self.BOX_ROLE)
        outbox_item.setData(UI_OUTBOX, self.BOX_ROLE)

        # Create filters for each child item
        for box in [inbox_item, outbox_item]:
            box.appendRow((create_sub_items(UI_STARRED_BOX)))
            box.appendRow((create_sub_items(UI_EXPIRED_BOX)))

        my_boxes_items.appendRow(inbox_item)
        my_boxes_items.appendRow(outbox_item)

        # Get all users form DB & populate users full names under all_users_items
        users = get_all_users()

        for user in users:
            user_id, first_name, last_name, email = user
            user_item = QStandardItem(f"{last_name} {first_name}")
            user_item.setData(user_id, self.USER_ROLE)
            user_item.setData(email, Qt.ToolTipRole)
            all_users_items.appendRow(user_item)

        self.tree_view.selectionModel().selectionChanged.connect(self.on_tree_item_selected)

        # Add Both Parent Items to the Tree Root
        root_item = self.tree_model.invisibleRootItem()
        root_item.appendRow(my_boxes_items)
        root_item.appendRow(all_users_items)

        # Expand all treeview
        self.tree_view.expandAll()

        # Add send task to treeview user by double-click
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)

        # Disable treeview modification
        self.set_treeview_readonly()

        # Create table view
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)  # Selects the entire row
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)  # Allows only one row at a time

        # Create a splitter and add both tree view and table view
        self.left_splitter = QSplitter(Qt.Horizontal)
        self.left_splitter.addWidget(self.tree_view)
        self.left_splitter.addWidget(self.table_view)
        self.left_splitter.setStretchFactor(0, 1)
        self.left_splitter.setStretchFactor(1, 2)

        # Left column: Task ID, Created At, Modified At
        left_meta_layout = QVBoxLayout()
        self.task_id_label = QLabel(f"{UI_TASK_ID}:")
        self.task_id_value = QLabel()
        self.created_at_label = QLabel(f"{UI_CREATED_AT}:")
        self.created_at_value = QLabel()
        self.modified_at_label = QLabel(f"{UI_MODIFIED_AT}:")
        self.modified_at_value = QLabel()
        left_meta_layout.addWidget(self.task_id_label)
        left_meta_layout.addWidget(self.task_id_value)
        left_meta_layout.addWidget(self.created_at_label)
        left_meta_layout.addWidget(self.created_at_value)
        left_meta_layout.addWidget(self.modified_at_label)
        left_meta_layout.addWidget(self.modified_at_value)

        # Right column: Sender, Receiver
        right_meta_layout = QVBoxLayout()
        self.sender_label = QLabel(f"{UI_SENDER}:")
        self.sender_full_name = QLabel()
        self.sender_email = QLabel(F'<a href="#">{""}</a>')
        self.sender_email.linkActivated.connect(lambda: send_email(email="", title=f"{APP_NAME}_{UI_TASK}_{100000}")) #

        self.receiver_label = QLabel(f"{UI_RECEIVER}:")
        self.receiver_full_name = QLabel()
        self.receiver_email = QLabel(f'<a href="#">{""}</a>')
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
        task_layout = QHBoxLayout()
        self.task_label = QLabel(f"{UI_TASK}:")
        self.starred_checkbox = QCheckBox(UI_STARRED)
        self.starred_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.starred_checkbox.setToolTip(UI_STARRED_TIP)
        self.archived_checkbox = QCheckBox(UI_ARCHIVED)
        self.archived_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.archived_checkbox.setToolTip(UI_ARCHIVED_TIP)
        task_layout.addWidget(self.task_label)
        task_layout.addStretch()
        task_layout.addWidget(self.starred_checkbox)
        task_layout.addWidget(self.archived_checkbox)
        main_vertical_layout.addLayout(task_layout)

        # Task title input
        self.title_input = QLineEdit()
        self.title_input.textChanged.connect(self.check_send_button)
        self.title_input.setReadOnly(True)
        main_vertical_layout.addWidget(self.title_input)

        # Task body input
        self.body_input = QTextEdit()
        self.body_input.setReadOnly(True)
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
        self.open_directory_action = QAction(UI_REFERENCE_OPEN, self)
        self.open_directory_action.triggered.connect(self.open_directory_dialog)
        self.copy_link_action = QAction(UI_REFERENCE_COPY, self)
        self.copy_link_action.triggered.connect(self.copy_reference_link)
        self.paste_link_action = QAction(UI_REFERENCE_PASTE, self)
        self.paste_link_action.triggered.connect(self.paste_reference_link)
        self.delete_link_action = QAction(UI_REFERENCE_DELETE, self)
        self.delete_link_action.triggered.connect(self.delete_reference_link)
        self.menu.addAction(self.open_directory_action)
        self.menu.addAction(self.copy_link_action)
        self.menu.addAction(self.paste_link_action)
        self.menu.addAction(self.delete_link_action)
        self.menu_button.setMenu(self.menu)

        # Due At
        due_at_layout = QHBoxLayout()
        self.due_at_label = QLabel(f"{UI_DUE_AT}:")
        self.due_at_days = QLabel("42")
        self.due_at_days.setAlignment(Qt.AlignRight)
        due_at_layout.addWidget(self.due_at_label)
        due_at_layout.addWidget(self.due_at_days)
        self.due_at_input = QDateTimeEdit()
        self.due_at_input.setDateTime(next_working_midday())
        self.due_at_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
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
        self.expected_at_input.setDateTime(next_working_midday())
        self.expected_at_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.expected_at_input.setCalendarPopup(True)
        main_vertical_layout.addLayout(expected_at_layout)
        main_vertical_layout.addWidget(self.expected_at_input)

        # Reply
        reply_layout = QHBoxLayout()
        self.reply_label = QLabel(f"{UI_REPLY}:")
        self.done_checkbox = QCheckBox(UI_DONE)
        self.done_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.done_checkbox.setToolTip(UI_DONE_TIP)
        reply_layout.addWidget(self.reply_label)
        reply_layout.addStretch()
        reply_layout.addWidget(self.done_checkbox)
        main_vertical_layout.addLayout(reply_layout)

        # Reply input
        self.reply_input = QTextEdit()
        self.reply_input.textChanged.connect(self.check_send_button)
        self.reply_input.setReadOnly(True)
        main_vertical_layout.addWidget(self.reply_input)

        # Add horizontal line between checkboxes and update button
        horizontal_line_3 = QFrame()
        horizontal_line_3.setFrameShape(QFrame.HLine)
        horizontal_line_3.setFrameShadow(QFrame.Sunken)
        main_vertical_layout.addWidget(horizontal_line_3)

        # Add send task button
        self.send_button_layout = QHBoxLayout()
        self.send_button = QPushButton(UI_SEND)
        self.send_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.send_button_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_task)
        main_vertical_layout.addLayout(self.send_button_layout)

        # Wrap everything in a QWidget for the splitter
        self.task_details_widget = QWidget(self)
        self.task_details_widget.setLayout(main_vertical_layout)

        # Create a splitter and add tree/table views and task details widget
        self.right_splitter = QSplitter(Qt.Horizontal)
        self.right_splitter.addWidget(self.left_splitter)
        self.right_splitter.addWidget(self.task_details_widget)
        self.right_splitter.setStretchFactor(0, 2)
        self.right_splitter.setStretchFactor(1, 1)

        # Set the splitter as the main layout
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.right_splitter)

        self.setCentralWidget(central_widget)

        # Create menu bar
        menu_bar = self.menuBar()
            # User Menu
        user_menu = menu_bar.addMenu(UI_USER_MENU)
        user_data_action = QAction(UI_USER_DATA, self)
        user_data_action.triggered.connect(self.show_user)
        user_menu.addAction(user_data_action)
            # Export Menu
        export_menu = menu_bar.addMenu(UI_EXPORT_MENU)
                # Personal
        personal_action = QAction(UI_PERSONAL_TASKS, self)
        export_menu.addAction(personal_action)
                # All
        all_action = QAction(UI_ALL_TASKS, self)
        export_menu.addAction(all_action)
            # Info Menu
                # About
        info_menu = menu_bar.addMenu(UI_INFO_MENU)
        about_action = QAction(UI_ABOUT, self)
        info_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about)
                # Help
        help_action = QAction(UI_HELP, self)
        info_menu.addAction(help_action)
        help_action.triggered.connect(self.show_readme)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.adjustSize()
        self.center()

        # Lists of UI elements to be disabled for inbox, outbox and send modes
        self.inbox_disabled_elements = [self.starred_checkbox, self.archived_checkbox, self.due_at_input,
                                        self.send_button, self.open_directory_action,
                                        self.paste_link_action, self.delete_link_action]
        self.outbox_disabled_elements = [self.expected_at_input, self.done_checkbox, self.send_button]
        self.send_disabled_elements = [self.done_checkbox, self.reply_label, self.reply_input, self.send_button,
                                       self.task_id_label, self.task_id_value, self.created_at_label,
                                       self.created_at_value, self.modified_at_label, self.modified_at_value]

        # Lists of UI elements to be reset and cleared in clear mode
        self.task_actions = [self.open_directory_action, self.copy_link_action, self.paste_link_action,
                             self.delete_link_action]
        self.clearable_elements = [self.task_id_value, self.created_at_value, self.modified_at_value,
                                   self.sender_full_name, self.sender_email, self.receiver_full_name,
                                   self.receiver_email, self.title_input, self.body_input, self.due_at_days,
                                   self.expected_at_days, self.reply_input]
        self.resettable_checkboxes = [self.starred_checkbox, self.archived_checkbox, self.done_checkbox]

        self.set_clear_mode() # Initially clear task details panel

        # Placeholders
        self.about_ui = None
        self.readme_ui = None
        self.update_ui = None

        # Attributes
        self.current_task_id = None
        self.new_receiver_id = None

    def set_treeview_readonly(self):
        """Disable editing for all items in the tree view."""
        for row in range(self.tree_model.rowCount()):
            parent_item = self.tree_model.item(row)
            parent_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editing

            for child_row in range(parent_item.rowCount()):
                child_item = parent_item.child(child_row)
                child_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editing

                for sub_row in range(child_item.rowCount()):
                    sub_item = child_item.child(sub_row)
                    sub_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editing

    def check_send_button(self):
        """Enables send button based if task title is not empty, otherwise, disables it."""
        if self.reply_input.isReadOnly():
            if self.title_input.text().strip():
                self.send_button.setEnabled(True)
            else:
                self.send_button.setEnabled(False)
        elif self.title_input.isReadOnly():
            if self.reply_input.toPlainText().strip():
                self.send_button.setEnabled(True)
            else:
                self.send_button.setEnabled(False)

    def on_table_row_selected(self):
        """Retrieve task ID from the selected row """
        index = self.table_view.selectionModel().currentIndex()
        id_col_index =  self.table_view.model().index(index.row(), 0)
        self.current_task_id = self.table_view.model().data(id_col_index, Qt.UserRole)
        task_details = get_task_details(self.current_task_id)

        self.task_id_value.setText(str(task_details[0]))
        sender_first_name,  sender_last_name = get_user_full_name(task_details[1])
        self.sender_full_name.setText(f"{sender_first_name} {sender_last_name}")
        self.sender_email.setText(get_user_email(task_details[1]))
        receiver_first_name, receiver_last_name = get_user_full_name(task_details[2])
        self.receiver_full_name.setText(f"{receiver_first_name} {receiver_last_name}")
        self.receiver_email.setText(get_user_email(task_details[2]))
        self.created_at_value.setText(task_details[3])
        self.modified_at_value.setText(task_details[4])
        self.title_input.setText(task_details[5])
        self.body_input.setText(task_details[6])
        self.reference_label.setText(f'<a href={task_details[7]}>{UI_REFERENCE}:</a>')
        self.reference_label.setToolTip(task_details[7])
        self.due_at_input.setDateTime(QDateTime.fromString(task_details[8],"yyyy-MM-dd HH:mm:ss"))
        if task_details[9]:
            self.starred_checkbox.setChecked(True)
        else:
            self.starred_checkbox.setChecked(False)
        if task_details[10]:
            self.done_checkbox.setChecked(True)
        else:
            self.done_checkbox.setChecked(False)
        self.expected_at_input.setDateTime(QDateTime.fromString(task_details[11],"yyyy-MM-dd HH:mm:ss"))
        self.reply_input.setText(task_details[12])
        if task_details[13]:
            self.archived_checkbox.setChecked(True)
        else:
            self.archived_checkbox.setChecked(False)
        self.send_button.setEnabled(False)

    def on_tree_item_selected(self):
        """Handles selecting a user item in the TreeView."""
        index = self.tree_view.selectionModel().currentIndex()

        user_id = index.data(self.USER_ROLE)
        box_type = index.data(self.BOX_ROLE)
        filter_type = index.data(self.FILTER_ROLE)

        if user_id:
            self.set_clear_mode() # Clear task details panel
            tasks = get_tasks(user_id=user_id, box_type=UI_INBOX)
            model = TaskTableModel(tasks)
            self.table_view.setModel(model)
        elif box_type:
            if box_type == UI_INBOX:
                self.set_inbox_mode()
            elif box_type == UI_OUTBOX:
                self.set_outbox_mode()
            tasks = get_tasks(user_id=config.my_id, box_type=box_type)
            model = TaskTableModel(tasks)
            self.table_view.setModel(model)
        elif filter_type:
            parent_index = index.parent()
            box_type = parent_index.data(self.BOX_ROLE)
            if box_type == UI_INBOX:
                self.set_inbox_mode()
            elif box_type == UI_OUTBOX:
                self.set_outbox_mode()
            tasks = get_tasks(user_id=config.my_id, box_type=box_type, filter_type=filter_type)
            model = TaskTableModel(tasks)
            self.table_view.setModel(model)
        else:
            model = TaskTableModel([])
            self.table_view.setModel(model)
            self.set_clear_mode()

        self.table_view.selectionModel().selectionChanged.connect(self.on_table_row_selected)

        self.adjust_tableview()

    def adjust_tableview(self):
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Default sizing
        self.table_view.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_view.setWordWrap(True)
        # self.table_view.resizeRowsToContents()
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def on_item_double_clicked(self, index):
        """Handles double-clicking a user item in the TreeView."""
        user_id = index.data(self.USER_ROLE)
        if user_id:
            self.new_receiver_id = user_id
            self.set_send_mode()

    def send_task(self):
        if self.current_task_id:
            update_result = update_task(sender_id=config.my_id,
                                        receiver_id=self.new_receiver_id,
                                        title=self.title_input.text(),
                                        body=self.body_input.toPlainText(),
                                        reference=self.reference_label.toolTip(),
                                        due_at=self.due_at_input.text(),
                                        expected_at=self.expected_at_input,
                                        starred=1 if self.starred_checkbox.isChecked() else 0,
                                        archived=1 if self.archived_checkbox.isChecked() else 0,
                                        reply=self.reply_input.text(),
                                        done=1 if self.done_checkbox.isChecked() else 0,
                                        task_id=self.current_task_id)
            print(update_result)
        else:
            new_task_id = add_task(sender_id=config.my_id,
                                   receiver_id=self.new_receiver_id,
                                   title=self.title_input.text(),
                                   body=self.body_input.toPlainText(),
                                   reference=self.reference_label.toolTip(),
                                   due_at=self.due_at_input.text(),
                                   expected_at=self.expected_at_input.text(),
                                   starred=1 if self.starred_checkbox.isChecked() else 0,
                                   archived=1 if self.archived_checkbox.isChecked() else 0)
            print(new_task_id)

    def enable_task_details(self, enabled_bool):
        for element in self.task_details_widget.findChildren(QWidget):
            element.setEnabled(enabled_bool)
        for action in self.task_actions:
            action.setEnabled(enabled_bool)

    def set_inbox_mode(self):
        self.enable_task_details(True)
        self.title_input.setReadOnly(True)
        self.body_input.setReadOnly(True)
        self.reply_input.setReadOnly(False)
        for element in self.inbox_disabled_elements:
            element.setEnabled(False)

    def set_outbox_mode(self):
        self.enable_task_details(True)
        self.title_input.setReadOnly(False)
        self.body_input.setReadOnly(False)
        self.reply_input.setReadOnly(True)
        for element in self.outbox_disabled_elements:
            element.setEnabled(False)

    def set_send_mode(self):
        self.current_task_id = None
        self.due_at_input.setDateTime(next_working_midday())
        self.expected_at_input.setDateTime(next_working_midday())
        self.enable_task_details(True)
        self.title_input.setReadOnly(False)
        self.body_input.setReadOnly(False)
        self.reply_input.setReadOnly(True)
        for element in self.send_disabled_elements:
            element.setEnabled(False)

    def set_clear_mode(self):
        self.due_at_input.setDateTime(next_working_midday())
        self.expected_at_input.setDateTime(next_working_midday())
        for element in self.clearable_elements:
            element.setText("")
        for checkbox in self.resettable_checkboxes:
            checkbox.setChecked(False)
        self.enable_task_details(False)

    def open_directory_dialog(self):
        directory_path = select_directory_dialog(parent=self, default_dir=get_directory(config.config[CFG_PATH]))
        self.reference_label.setText(f'<a href={directory_path}>{UI_REFERENCE}:</a>')
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
        self.reference_label.setText(f'<a href={pasted_text}>{UI_REFERENCE}:</a>')
        self.reference_label.setToolTip(pasted_text)
        if pasted_text:
            self.status_bar.showMessage(f"{UI_PASTED}: {pasted_text}")

    def delete_reference_link(self):
        deleted_text = self.reference_label.toolTip()
        self.reference_label.setText(F"{UI_REFERENCE}:")
        self.reference_label.setToolTip("")
        if deleted_text:
            self.status_bar.showMessage(f"{UI_DELETED}: {deleted_text}")

    def show_user(self):
        if self.update_ui is None:
            self.update_ui = UserUpdate()
        self.update_ui.show()

    def show_about(self):
        if self.about_ui is None:
            self.about_ui = AboutScreen()
        self.about_ui.show()

    def show_readme(self):
        if self.readme_ui is None:
            self.readme_ui = ReadmeViewer()
        self.readme_ui.show()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def closeEvent(self, event):
        response = show_question_msg(text=MSG_CLOSE)
        if response:
            sys.exit()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
