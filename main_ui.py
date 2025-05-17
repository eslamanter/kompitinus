import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QTableView, QSplitter, QLineEdit,
    QTextEdit, QCheckBox, QPushButton, QDateTimeEdit, QTreeView, QStatusBar, QMenu, QAction, QToolButton,
    QHeaderView, QAbstractItemView, QCalendarWidget)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor, QBrush, QColor, QTextCharFormat
from PyQt5.QtCore import Qt, QDateTime, QDate
from readme_ui import ReadmeViewer
from about_ui import AboutScreen
from constants import *
from sqlite_db import (get_all_users, add_task, update_task, get_tasks, get_task_details, get_user_full_name,
                       get_user_email, export_report_view)
from user_ui import UserUpdate
from utils import (send_email, select_directory_dialog, get_directory, show_question_msg, next_working_midday,
                   count_days, playsound_ok)
from datetime import date
import config
import holidays


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
            due_at_item = QStandardItem(due_at[:16].replace(" ", "\n"))

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
        self.left_splitter.setStretchFactor(1, 3)

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
        self.sender_email = QLabel()

        self.receiver_label = QLabel(f"{UI_RECEIVER}:")
        self.receiver_full_name = QLabel()
        self.receiver_email = QLabel()

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
        self.title_input.setMaxLength(UI_MAX_TITLE_LEN)
        self.title_input.setPlaceholderText(UI_PLACEHOLDER_TITLE)
        self.title_input.setReadOnly(True)
        main_vertical_layout.addWidget(self.title_input)

        # Task body input
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText(UI_PLACEHOLDER_BODY)
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
        self.due_at_days = QLabel()
        self.due_at_days.setAlignment(Qt.AlignRight)
        due_at_layout.addWidget(self.due_at_label)
        due_at_layout.addWidget(self.due_at_days)
        self.due_at_input = QDateTimeEdit()
        self.due_at_input.setDateTime(next_working_midday())
        self.due_at_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.due_at_input.setCalendarPopup(True)
        main_vertical_layout.addLayout(due_at_layout)
        main_vertical_layout.addWidget(self.due_at_input)

        # Expected At
        expected_at_layout = QHBoxLayout()
        self.expected_at_label = QLabel(f"{UI_EXPECTED_AT}:")
        self.expected_at_days = QLabel()
        self.expected_at_days.setAlignment(Qt.AlignRight)
        expected_at_layout.addWidget(self.expected_at_label)
        expected_at_layout.addWidget(self.expected_at_days)
        self.expected_at_input = QDateTimeEdit()
        self.expected_at_input.setDateTime(next_working_midday())
        self.expected_at_input.setDisplayFormat("yyyy-MM-dd HH:mm")
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
        self.reply_input.setPlaceholderText(UI_PLACEHOLDER_REPLY)
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
                # All
        export_all_action = QAction(UI_STARRED_BOX, self)
        export_menu.addAction(export_all_action)
        export_all_action.triggered.connect(lambda: export_report_view())
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

        # Lists of task UI elements to be disabled for inbox, outbox and send modes
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
        self.labels = [self.task_id_value, self.created_at_value, self.modified_at_value,
                       self.sender_full_name, self.sender_email, self.receiver_full_name,
                       self.receiver_email, self.due_at_days, self.expected_at_days]
        self.text_inputs = [self.title_input, self.body_input, self.reply_input]
        self.date_time_inputs = [self.due_at_input, self.expected_at_input] # Not to clear but to show following midday
        self.clearable_elements = self.labels + self.text_inputs # To clear by setting text as ""
        self.resettable_checkboxes = [self.starred_checkbox, self.archived_checkbox, self.done_checkbox] # To reset by unchecking

        self.set_clear_mode() # Initially clear task details panel

        # Placeholders
        self.about_ui = None
        self.readme_ui = None
        self.update_ui = None

        # Attributes
        self.current_task_id = None # Stores current task ID. Stores None if no task selected or upon sending a new task
        self.new_receiver_id = None # Stores new task receiver user ID. Stores None if task exists

        # Setup calendars to highlight Italy holidays in red
        current_year = QDate.currentDate().year()
        self.italy_holidays = holidays.Italy(years=[current_year, current_year + 1])
        self.setup_calendars()

        # Connect input changes to send button enabling/update days to deadline
        for date_time_input in self.date_time_inputs:
            date_time_input.dateTimeChanged.connect(self.check_send_button)
            date_time_input.dateTimeChanged.connect(self.update_due_expected_days)
        for text_input in self.text_inputs:
            text_input.textChanged.connect(self.check_send_button)
        for checkbox in self.resettable_checkboxes:
            checkbox.stateChanged.connect(self.check_send_button)
        self.done_checkbox.stateChanged.connect(self.update_due_expected_days)

    def highlight_selected_deadlines(self):
        selected_datetime_due = self.due_at_input.dateTime()
        selected_datetime_expected = self.expected_at_input.dateTime()

        # Convert to QDate & QTime for checks
        selected_date_due = selected_datetime_due.date()
        selected_time_due = selected_datetime_due.time()

        selected_date_expected = selected_datetime_expected.date()
        selected_time_expected = selected_datetime_expected.time()

        # Check if the selected date is a holiday or weekend
        def is_special_date(qdate):
            # Convert QDate to Python date
            py_date = date(qdate.year(), qdate.month(), qdate.day())
            # Check if it's a holiday or weekend
            return py_date in self.italy_holidays or qdate.dayOfWeek() in [6, 7]  # Saturday = 6, Sunday = 7

        # Check if time is outside working hours (before 09:00 or after 19:00)
        def is_outside_working_hours(qtime):
            return qtime.hour() < WORKING_HOURS[0] or qtime.hour() > WORKING_HOURS[1]

        # Apply red color if it's a holiday, weekend, or outside working hours
        if is_special_date(selected_date_due):
            due_style = "color: red;"
            self.due_at_input.setToolTip(UI_HOLIDAY)
        elif is_outside_working_hours(selected_time_due):
            due_style = "color: red;"
            self.due_at_input.setToolTip(UI_OUTSIDE_HOURS)
        else:
            due_style = "color: black;"
            self.due_at_input.setToolTip("")

        if is_special_date(selected_date_expected):
            expected_style = "color: red;"
            self.expected_at_input.setToolTip(UI_HOLIDAY)
        elif is_outside_working_hours(selected_time_expected):
            expected_style = "color: red;"
            self.expected_at_input.setToolTip(UI_OUTSIDE_HOURS)
        else:
            expected_style = "color: black;"
            self.expected_at_input.setToolTip("")

        self.due_at_input.setStyleSheet(due_style)
        self.expected_at_input.setStyleSheet(expected_style)

    def setup_calendars(self):
        """Sets up calendars to highlight Italy holidays."""
        # Get the calendar widget from QDateTimeEdit (popup instance)
        due_at_calendar = self.due_at_input.calendarWidget()
        expected_at_calendar = self.expected_at_input.calendarWidget()

        # Format for holidays (red text)
        holiday_format = QTextCharFormat()
        holiday_format.setForeground(QColor("red"))

        # Apply formatting to holiday dates
        for date in self.italy_holidays.keys():
            qdate = QDate(date.year, date.month, date.day)
            due_at_calendar.setDateTextFormat(qdate, holiday_format)
            expected_at_calendar.setDateTextFormat(qdate, holiday_format)

        self.due_at_input.dateTimeChanged.connect(self.highlight_selected_deadlines)
        self.expected_at_input.dateTimeChanged.connect(self.highlight_selected_deadlines)

    def update_due_expected_days(self):
        due_at = self.due_at_input.text() + ":00"
        days_to_due = count_days(deadline=due_at)
        expected_at = self.expected_at_input.text() + ":00"
        days_to_expected = count_days(deadline=expected_at)

        if self.done_checkbox.isChecked():
            self.due_at_days.setText("")
            self.expected_at_days.setText("")
        else:
            self.due_at_days.setText(f"{days_to_due} {UI_DAYS}")
            if days_to_due < 0:
                self.due_at_days.setStyleSheet("color: red;")
            else:
                self.due_at_days.setStyleSheet("color: black;")
            self.expected_at_days.setText(f"{days_to_expected} {UI_DAYS}")
            if days_to_expected < 0:
                self.expected_at_days.setStyleSheet("color: red;")
            else:
                self.expected_at_days.setStyleSheet("color: black;")

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
        if self.current_task_id or self.new_receiver_id:
            if self.title_input.text().strip():
                self.send_button.setEnabled(True)
            else:
                self.send_button.setEnabled(False)

    def show_sender_receiver_info(self,sender_id, receiver_id, task_id=""):
        sender_first_name, sender_last_name = get_user_full_name(sender_id)
        self.sender_full_name.setText(f"{sender_first_name} {sender_last_name}")
        sender_email = get_user_email(sender_id)
        self.sender_email.setText(f'<a href="#">{sender_email}</a>')
        self.sender_email.setToolTip(f"{UI_SEND_EMAIL_TO} {sender_email}")
        self.sender_email.linkActivated.connect(
            lambda: send_email(email=sender_email, title=f"{UI_TASK} {task_id}"))

        receiver_first_name, receiver_last_name = get_user_full_name(receiver_id)
        self.receiver_full_name.setText(f"{receiver_first_name} {receiver_last_name}")
        receiver_email = get_user_email(receiver_id)
        self.receiver_email.setText(f'<a href="#">{receiver_email}</a>')
        self.receiver_email.setToolTip(f"{UI_SEND_EMAIL_TO} {receiver_email}")
        self.receiver_email.linkActivated.connect(
            lambda: send_email(email=receiver_email, title=f"{UI_TASK} {task_id}"))

    def on_table_row_selected(self):
        """Retrieve task ID from the selected row and fill task details panel."""
        item_index = self.table_view.selectionModel().currentIndex()
        id_col_index =  self.table_view.model().index(item_index.row(), 0)
        self.current_task_id = self.table_view.model().data(id_col_index, Qt.UserRole)

        task_details = get_task_details(self.current_task_id)
        (task_id, sender_id, receiver_id, created_at, modified_at, title, body,
         reference, due_at, starred, done, expected_at, reply, archived) = task_details

        self.task_id_value.setText(str(task_id))
        self.show_sender_receiver_info(task_id=task_id, sender_id=sender_id, receiver_id=receiver_id)

        self.created_at_value.setText(created_at)
        self.modified_at_value.setText(modified_at)

        self.title_input.setText(title)
        self.body_input.setText(body)
        self.reply_input.setText(reply)

        self.reference_label.setText(f'<a href={reference}>{UI_REFERENCE}:</a>')
        self.reference_label.setToolTip(reference)

        self.due_at_input.setDateTime(QDateTime.fromString(due_at[:16],"yyyy-MM-dd HH:mm"))
        self.expected_at_input.setDateTime(QDateTime.fromString(expected_at[:16], "yyyy-MM-dd HH:mm"))

        self.starred_checkbox.setChecked(bool(starred))
        self.done_checkbox.setChecked(bool(done))
        self.archived_checkbox.setChecked(bool(archived))

        self.send_button.setEnabled(False)
        self.update_due_expected_days()
        self.highlight_selected_deadlines()

    def on_tree_item_selected(self):
        """Handles selecting a user item in the TreeView."""
        index = self.tree_view.selectionModel().currentIndex()

        user_id = index.data(self.USER_ROLE) # User selection
        box_type = index.data(self.BOX_ROLE) # Inbox/Outbox selection
        filter_type = index.data(self.FILTER_ROLE) # Starred/Expired filter selection

        self.set_clear_mode()  # Clear task details panel

        if user_id:
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
            self.table_view.selectionModel().selectionChanged.connect(self.on_table_row_selected)
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
            self.table_view.selectionModel().selectionChanged.connect(self.on_table_row_selected)
        else:
            model = TaskTableModel([])
            self.table_view.setModel(model)

        self.adjust_tableview()

    def adjust_tableview(self):
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Default sizing
        self.table_view.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_view.setWordWrap(True)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def on_item_double_clicked(self, index):
        """Handles double-clicking a user item in the TreeView."""
        user_id = index.data(self.USER_ROLE)
        if user_id:
            self.new_receiver_id = user_id
            self.show_sender_receiver_info(config.my_id, self.new_receiver_id)
            self.update_due_expected_days()
            self.highlight_selected_deadlines()
            self.set_send_mode()

    def send_task(self):
        self.send_button.setEnabled(False)
        if self.current_task_id:
            update_result = update_task(title=self.title_input.text().upper(),
                                        body=self.body_input.toPlainText(),
                                        reference=self.reference_label.toolTip(),
                                        due_at=self.due_at_input.text() + ":00",
                                        expected_at=self.expected_at_input.text() + ":00",
                                        starred=1 if self.starred_checkbox.isChecked() else 0,
                                        archived=1 if self.archived_checkbox.isChecked() else 0,
                                        reply=self.reply_input.toPlainText(),
                                        done=1 if self.done_checkbox.isChecked() else 0,
                                        task_id=self.current_task_id)
            if update_result:
                playsound_ok()
                self.status_bar.showMessage(f"{UI_TASK} {self.current_task_id} {UI_TASK_UPDATED}")
                # Select a dummy index then the previously selected index of the TreeView to update the TableView
                previous_index = self.tree_view.selectionModel().currentIndex()
                dummy_index = self.tree_model.index(0, 0)
                self.tree_view.setCurrentIndex(dummy_index)
                self.tree_view.setCurrentIndex(previous_index)
            else:
                self.send_button.setEnabled(True)
        else:
            new_task_id = add_task(sender_id=config.my_id,
                                   receiver_id=self.new_receiver_id,
                                   title=self.title_input.text().upper(),
                                   body=self.body_input.toPlainText(),
                                   reference=self.reference_label.toolTip(),
                                   due_at=self.due_at_input.text() + ":00",
                                   expected_at=self.expected_at_input.text() + ":00",
                                   starred=1 if self.starred_checkbox.isChecked() else 0,
                                   archived=1 if self.archived_checkbox.isChecked() else 0)
            if new_task_id:
                playsound_ok()
                self.status_bar.showMessage(f"{UI_TASK} {new_task_id} {UI_TASK_SENT}")
                # Select the Outbox index of the TreeView to show the updated TableView
                outbox_index = self.tree_model.index(1, 0, self.tree_model.index(0, 0))
                self.tree_view.setCurrentIndex(outbox_index)
            else:
                self.send_button.setEnabled(True)

    def enable_task_details(self, enabled_bool):
        for element in self.task_details_widget.findChildren(QWidget):
            element.setEnabled(enabled_bool)
        for action in self.task_actions:
            action.setEnabled(enabled_bool)

    def set_inbox_mode(self):
        self.current_task_id = None
        self.new_receiver_id = None
        self.enable_task_details(True)
        self.title_input.setReadOnly(True)
        self.body_input.setReadOnly(True)
        self.reply_input.setReadOnly(False)
        for element in self.inbox_disabled_elements:
            element.setEnabled(False)

    def set_outbox_mode(self):
        self.current_task_id = None
        self.new_receiver_id = None
        self.enable_task_details(True)
        self.title_input.setReadOnly(False)
        self.body_input.setReadOnly(False)
        self.reply_input.setReadOnly(True)
        for element in self.outbox_disabled_elements:
            element.setEnabled(False)

    def set_send_mode(self):
        self.current_task_id = None
        for date_time_input in self.date_time_inputs:
            date_time_input.setDateTime(next_working_midday())
        self.enable_task_details(True)
        self.title_input.setReadOnly(False)
        self.body_input.setReadOnly(False)
        self.reply_input.setReadOnly(True)
        for element in self.send_disabled_elements:
            element.setEnabled(False)

    def set_clear_mode(self):
        for date_time_input in self.date_time_inputs:
            date_time_input.setDateTime(next_working_midday())
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
            self.check_send_button()

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
            self.check_send_button()

    def delete_reference_link(self):
        deleted_text = self.reference_label.toolTip()
        self.reference_label.setText(F"{UI_REFERENCE}:")
        self.reference_label.setToolTip("")
        if deleted_text:
            self.status_bar.showMessage(f"{UI_DELETED}: {deleted_text}")
            self.check_send_button()

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
