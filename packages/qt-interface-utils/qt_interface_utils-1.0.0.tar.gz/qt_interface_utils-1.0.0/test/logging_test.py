import logging
import threading
import time

from qt_interface_utils.log import QDockableLoggingWidget
from qtpy import QtWidgets


def log_thread(name: str):
    logger = logging.getLogger(name)

    while True:
        logger.debug(f"{name} debug")
        logger.info(f"{name} info")
        logger.warning(f"{name} warning")
        logger.error(f"{name} error")
        logger.critical(f"{name} critical")
        time.sleep(1)


class Gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        self.log = logging.getLogger()
        self.log_widget = QDockableLoggingWidget()
        self.log_widget.register_logger(self.log)
        self.setCentralWidget(self.log_widget)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Gui()
    gui.show()

    # Start loggers
    threading.Thread(target=log_thread, args=("Thread1",), daemon=True).start()
    threading.Thread(target=log_thread, args=("Thread2",), daemon=True).start()
    threading.Thread(target=log_thread, args=("Thread2.logy",), daemon=True).start()
    sys.exit(app.exec_())
