from qtpy.QtWidgets import QDialog, QTextEdit, QVBoxLayout

from .messaging import catch_exception


class LicenseDialog:
    def __init__(self, parent, application_context):
        self.parent = parent
        self.application_context = application_context

    @catch_exception("Failed to show license dialog")
    def show(self):
        """Build and show the license window"""

        # QMessageBox.aboutQt(self,"dfez")
        with open(self.application_context.get_resource("license.txt")) as f:
            dialog = QDialog()
            dialog.setWindowTitle("License")
            dialog.setFixedSize(500, 500)

            textbox = QTextEdit()
            textbox.setReadOnly(True)
            textbox.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
            textbox.setText(f.read())

            font = textbox.font()
            font.setFamily("Courier")
            font.setPointSize(3)

            layout = QVBoxLayout()
            layout.addWidget(textbox)
            dialog.setLayout(layout)

            dialog.exec_()
