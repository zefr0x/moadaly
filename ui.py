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

        self.setMinimumSize(1000, 700)
        self.setWindowTitle(_("Moadaly"))

        main_window_layout = QtWidgets.QVBoxLayout()

        top_boxes_layout = QtWidgets.QHBoxLayout()

        # Create main window widgets.
        self.result_box = ResultBox()
        self.previous_gpa_box = PreviousGPABox()
        self.calculation_system_box = CalculationSystemBox()

        # Add main components to the main window layout.
        top_boxes_layout.addWidget(self.result_box)
        top_boxes_layout.addWidget(self.previous_gpa_box)
        top_boxes_layout.addWidget(self.calculation_system_box)

        main_window_layout.addLayout(top_boxes_layout)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(main_window_layout)
        self.setCentralWidget(centralWidget)


class ResultBox(QtWidgets.QWidget):
    """A Group Box where the results are displayed, such as, GPA, grade, total hours and points."""

    def __init__(self):
        """Initialize components of the results widget."""
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


class PreviousGPABox(QtWidgets.QWidget):
    """A Group Box where you can specify a previous GPA, to add it to the calculation."""

    def __init__(self):
        """Initialize components of the previous GPA widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Previous GPA"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QGridLayout()

        # Previous Hours.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Previous Hours:")), 0, 0)
        self.previous_hours = QtWidgets.QLineEdit()
        self.previous_hours.setValidator(QtGui.QIntValidator(bottom=0))
        group_box_layout.addWidget(self.previous_hours, 0, 1)

        # Previous GPA.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Previous GPA:")), 1, 0)
        self.previous_gpa = QtWidgets.QLineEdit()
        # TODO Set the maximum value to 4 or 5 for the GPA depending on the used GPA system.
        self.previous_gpa.setValidator(QtGui.QDoubleValidator(bottom=0))
        group_box_layout.addWidget(self.previous_gpa, 1, 1)

        group_box.setLayout(group_box_layout)


class CalculationSystemBox(QtWidgets.QWidget):
    """A Group Box where you can specify the GPA calculation system."""

    def __init__(self):
        """Initialize components of the calculation system widget."""
        super().__init__()

        main_group_box = QtWidgets.QGroupBox(_("Calculation System"))
        main_group_box.setParent(self)

        group_box_layout = QtWidgets.QHBoxLayout()

        group_box_layout.addWidget(self.init_point_scale_box())
        group_box_layout.addWidget(self.init_grading_system_box())

        main_group_box.setLayout(group_box_layout)

    def init_point_scale_box(self) -> QtWidgets.QGroupBox:
        """Create point scale setting box."""
        point_scale_group_box = QtWidgets.QGroupBox(_("Point Scale"))
        point_scale_group_box_layout = QtWidgets.QVBoxLayout()

        radio_five_system = QtWidgets.QRadioButton("5.000")
        radio_five_system.setChecked(True)
        point_scale_group_box_layout.addWidget(radio_five_system)

        radio_four_system = QtWidgets.QRadioButton("4.000")
        point_scale_group_box_layout.addWidget(radio_four_system)
        # TODO Enable the option when the 4 point scale system is implemented.
        radio_four_system.setDisabled(True)

        point_scale_group_box.setLayout(point_scale_group_box_layout)

        return point_scale_group_box

    def init_grading_system_box(self) -> QtWidgets.QGroupBox:
        """Create grading system setting box."""
        point_scale_group_box = QtWidgets.QGroupBox(_("Grading System"))
        point_scale_group_box_layout = QtWidgets.QVBoxLayout()

        radio_normal_system = QtWidgets.QRadioButton(_("Normal"))
        radio_normal_system.setChecked(True)
        point_scale_group_box_layout.addWidget(radio_normal_system)

        radio_curve_system = QtWidgets.QRadioButton(_("Curve"))
        point_scale_group_box_layout.addWidget(radio_curve_system)
        # TODO Enable the option when the curve grading system is implemented.
        radio_curve_system.setDisabled(True)

        point_scale_group_box.setLayout(point_scale_group_box_layout)

        return point_scale_group_box


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
