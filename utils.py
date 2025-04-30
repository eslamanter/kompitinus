from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from about import DEV_EMAIL, APP_NAME, APP_VERSION

def send_email(email=DEV_EMAIL, title=f"{APP_NAME}_{APP_VERSION}"):
    mailto_link = f"mailto:{email}?subject=[{title}] "
    QDesktopServices.openUrl(QUrl(mailto_link))
