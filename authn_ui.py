import sys
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGroupBox,
                             QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from about import APP_NAME
from constants import UI_EMAIL, UI_LOGIN, UI_SIGNUP, UI_PIN
from utils import playsound_hand
from user_ui import UserSignup
import bcrypt

# # Hashing a password
# password = "MySecurePassword".encode('utf-8')
# hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
#
# # Verifying a password
# if bcrypt.checkpw(password, hashed_password):
#     print("Password is correct!")
