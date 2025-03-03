import logging
import sys
import traceback

from pydantic import BaseModel
from qtpy import QtWidgets


class Error(BaseModel):
    trace: str
    error: str

    @classmethod
    def from_exception(cls, e: Exception):
        return cls(trace=traceback.format_exc(), error=e.__repr__())

    def to_result(self) -> "Result":
        return Result(result=self)


class Success(BaseModel):
    message: str

    def to_result(self) -> "Result":
        return Result(result=self)


class Result(BaseModel):
    result: Error | Success

    def display(self, parent: QtWidgets.QWidget, title: str | None = None):
        if isinstance(self.result, Success):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText(self.result.message)
            msg.setStyleSheet("QMessageBox { messagebox-text-interaction-flags: 5; font-family: monospace; } ")
            msg.setWindowTitle("Success")
            # msg.setDetailedText("")
            msg.exec_()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setText(self.result.error)
            msg.setStyleSheet("QMessageBox { messagebox-text-interaction-flags: 5; font-family: monospace; } ")
            if title is not None:
                msg.setWindowTitle(title)
            else:
                msg.setWindowTitle("Error")
            msg.setDetailedText(self.result.trace)

            # Make the dialog wider
            horizontalSpacer = QtWidgets.QSpacerItem(
                350, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
            )
            layout = msg.layout()
            assert isinstance(layout, QtWidgets.QGridLayout)

            layout.addItem(horizontalSpacer, layout.rowCount(), 0, 1, layout.columnCount())

            # Add button to not show again, This doesn't work anymore
            # msg.addButton("Don't show again", QtWidgets.QMessageBox.ActionRole)

            # Add ok button
            msg.addButton(QtWidgets.QMessageBox.StandardButton.Ok)
            _ret = msg.exec_()

            # if ret == 0:
            #     self.ignored_errors.append(self.result.error)


def catch_exception(title):
    def decorator(f):
        def wrapped(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                Error.from_exception(e).to_result().display(self, title)
                logger = logging.getLogger(__name__)
                logger.exception("Error in function %s", f.__name__)

        return wrapped

    return decorator
