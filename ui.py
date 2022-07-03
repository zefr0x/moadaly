#!/usr/bin/python3
"""Main file for the GUI."""
import gettext

# import dbus
from PySide6 import QtCore, QtWidgets, QtGui

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

        main_window_layout = QtWidgets.QHBoxLayout()

        # Create main window widgets.
        result_box = ResultBox()

        # Add main components to the main window layout.
        main_window_layout.addWidget(result_box)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(main_window_layout)

        self.setCentralWidget(centralWidget)


class ResultBox(QtWidgets.QWidget):
    """A Group Box where the results are displayed, such as, GPA, grade, total hours and points."""

    def __init__(self):
        """Initialize main components of the results widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Result"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QGridLayout()

        # Result GPA.
        group_box_layout.addWidget(QtWidgets.QLabel(_("GPA:")), 0, 0)
        self.result_gpa = QtWidgets.QLabel(_("Undefined"))
        self.result_gpa.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_gpa, 0, 1)

        # Result hours.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Hours:")), 1, 0)
        self.result_hours = QtWidgets.QLabel("0")
        self.result_hours.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_hours, 1, 1)

        # Result points.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Points:")), 2, 0)
        self.result_points = QtWidgets.QLabel("0.00")
        self.result_points.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_points, 2, 1)

        # Result grade.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Grade:")), 3, 0)
        self.result_grade = QtWidgets.QLabel(_("Undefined"))
        self.result_grade.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_grade, 3, 1)

        group_box.setLayout(group_box_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
