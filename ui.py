#!/usr/bin/python3
"""Main file for the GUI."""
import gettext

import dbus
from PySide6 import QtWidgets, QtGui

import database


# TODO Configure it to use the "/usr/share/locale" directory.
gettext.bindtextdomain("moadaly", "locale")
gettext.textdomain("moadaly")
_ = gettext.gettext


class MainWindow(QtWidgets.QMainWindow):
    """Main window."""

    def __init__(self):
        """Initialize main components of the window."""
        super().__init__()

        self.setMinimumSize(800, 500)
        self.setWindowTitle(_("Moadaly"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
