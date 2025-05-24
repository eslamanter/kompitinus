import sys
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from markdown import markdown
from constants import APP_NAME, UI_README_TITLE, README_URL, MAIN_ICON


class ReadmeViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {UI_README_TITLE}")
        self.setWindowIcon(QIcon(MAIN_ICON))

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Add a QWebEngineView to display the README
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Fetch and display the README content
        self.fetch_and_display_readme()

        # Set the central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.web_view.setContextMenuPolicy(Qt.NoContextMenu) # Disable context menu

    def fetch_and_display_readme(self):
        try:
            response = requests.get(README_URL)
            response.raise_for_status()  # Raise an error for bad responses
            markdown_content = response.text

            # Convert markdown to HTML
            html_content = markdown(markdown_content)

            # Optionally, style the HTML (e.g., center-align content)
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        padding: 20px;
                        background-color: #f5f5f5;
                        color: #333;
                    }}
                    h1, h2, h3 {{
                        color: #2a7ae2;
                    }}
                    a {{
                        color: #1e88e5;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            self.web_view.setHtml(styled_html)
        except Exception as e:
            error_message = f"<html><body><h1>Failed to load README.md</h1><p>{e}</p></body></html>"
            self.web_view.setHtml(error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ReadmeViewer()
    viewer.show()
    sys.exit(app.exec_())
