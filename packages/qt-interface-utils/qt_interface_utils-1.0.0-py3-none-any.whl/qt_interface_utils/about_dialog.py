import sys

from qtpy.QtCore import QObject
from qtpy.QtWidgets import QMessageBox, QWidget


class QAboutDialog(QObject):
    def __init__(self, parent: QWidget, information: dict[str, str]):
        super().__init__()
        self._parent = parent
        self.information = information

    def show(self):
        """Build and show the about window"""
        version = self.information["full_version"]
        author = self.information["author"]
        environment = self.information["environment"]
        copyright = self.information["copyright"]
        app_name = self.information["app_name"]

        text = f"""<center>
                    <h1>{app_name}</h1>
                    </center>
                    <p>Version: {version}<br/>
                    Author: {author}<br/>
                    Enviroment: {environment}<br/>
                    Copyright &copy; {copyright}<br/>
                    Python: {sys.version}</p>
                    """

        QMessageBox.about(self._parent, "About", text)
