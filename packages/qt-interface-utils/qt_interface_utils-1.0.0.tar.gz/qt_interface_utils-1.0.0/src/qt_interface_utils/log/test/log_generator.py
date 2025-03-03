import logging
import threading
import time


class TestLogGenerator:
    def __init__(self):
        self.log_thread = threading.Thread(target=self.log_generator)
        self.log_thread.start()
        self.exception_thread = threading.Thread(target=self.exception_generator)
        self.exception_thread.start()

    def log_generator(self):
        logger = logging.getLogger("test")
        while True:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
            time.sleep(1)

    def exception_generator(self):
        logger = logging.getLogger("test")
        while True:
            try:
                raise ValueError("This is a test exception")
            except ValueError:
                logger.exception("An exception occurred")
            time.sleep(4.5)
