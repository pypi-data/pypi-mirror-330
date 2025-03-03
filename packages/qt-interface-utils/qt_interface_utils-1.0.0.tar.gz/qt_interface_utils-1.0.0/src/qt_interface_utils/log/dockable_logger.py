import logging
from functools import cached_property

from pydantic import BaseModel
from qtpy import QtWidgets
from qtpy.QtCore import QObject, Signal
from qtpy.QtGui import QColor


class QDockableLoggingWidget(QtWidgets.QDockWidget):
    class Config(BaseModel):
        max_log_lines: int = 1000

    config: Config

    def __init__(self, config: Config | None = None, font=None):
        if config is None:
            config = self.Config()
        super().__init__(parent=None)  # type: ignore
        self.setWindowTitle("Python Logger")

        self.config = config

        # Configure the text edit
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setAutoFillBackground(False)
        self.text_edit.setStyleSheet("QTextEdit {background-color:rgb(30, 30, 30);\ncolor: white }")
        self.text_edit.setReadOnly(True)
        self.text_edit.document().setMaximumBlockCount(self.config.max_log_lines)

        if font is not None:
            self.text_edit.setFont(font)

        # Create the log handler
        self.log_handler = LogHandler()
        self.log_handler.setFormatter(ConsoleFormatter())
        self.log_handler.data_signal.connect(self.append_text_to_output)

        # if self.Config.enable_file_logging:
        #     # create a rotating log file handler
        #     filename = f"python_log_{time.strftime('%Y%m%d-%H%M%S')}.log"
        #     self.log_file_handler = RotatingFileHandler(
        #         filename=os.path.join(self.Config.log_path, filename), maxBytes=5 * 1024 * 1024, backupCount=30
        #     )

        #     self.log_file_handler.setFormatter(
        #         logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        #     )
        #     self.log_file_handler.setLevel(logging.DEBUG)

        # Set central widget
        self.setWidget(self.text_edit)

    def register_logger(self, logger: logging.Logger):
        logger.addHandler(self.log_handler)
        # if self.config.enable_file_logging:
        #     logger.addHandler(self.log_file_handler)

    def append_text_to_output(self, text):
        """Append text to the output text box"""
        self.text_edit.append(text)


class ConsoleFormatter(logging.Formatter):
    FORMATS = {
        logging.ERROR: ("[ERR ]", QColor(255, 100, 100)),
        logging.DEBUG: ("[DBG ]", QColor(200, 200, 200)),
        logging.INFO: ("[INFO]", QColor(100, 250, 100)),
        logging.WARNING: ("[WARN]", QColor(255, 255, 50)),
        logging.CRITICAL: ("[CRIT]", QColor(255, 0, 0)),
    }

    def format(self, record):
        """Format logs"""
        opt = ConsoleFormatter.FORMATS.get(record.levelno)

        if opt:
            prefix, color = opt
            color = QColor(color).name()
        else:
            prefix, color = "[????]", QColor(255, 255, 255).name()

        self._style._fmt = f'<font color="{QColor(color).name()}">{prefix} (%(name)s) </font> %(message)s'

        res = logging.Formatter.format(self, record)

        # Replace newlines with <br>x
        res = res.replace("\n", "<br>")

        return res


class LogHandler(logging.Handler, QObject):
    # This is need to transition whatever thread that called to the QT thread
    data_signal = Signal(str)

    class _brigde(QObject):
        log = Signal(str)

    def __init__(self):
        super().__init__()
        self.data_signal = self.bridge.log

    @cached_property
    def bridge(self):
        return self._brigde()

    def emit(self, record):  # type: ignore
        msg = self.format(record)
        self.bridge.log.emit(msg)
