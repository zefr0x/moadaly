"""The result box where the results are displayed."""
from gettext import gettext as _

from PySide6 import QtCore, QtWidgets


class ResultBox(QtWidgets.QWidget):
    """A Group Box where the results are displayed, such as, GPA, grade, total hours and points."""

    def __init__(self):
        """Initialize components of the results widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Result"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QFormLayout()

        # Result GPA.
        self.result_gpa = QtWidgets.QDoubleSpinBox()
        self.result_gpa.setReadOnly(True)
        self.result_gpa.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.result_gpa.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.result_gpa.setDecimals(3)
        self.result_gpa.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("CGPA:")), self.result_gpa)

        # Result hours.
        self.result_hours = QtWidgets.QSpinBox()
        self.result_hours.setReadOnly(True)
        self.result_hours.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.result_hours.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.result_hours.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("Hours:")), self.result_hours)

        # Result points.
        self.result_points = QtWidgets.QDoubleSpinBox()
        self.result_points.setReadOnly(True)
        self.result_points.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.result_points.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.result_points.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("Points:")), self.result_points)

        # Result grade.
        self.result_grade = QtWidgets.QLabel(_("Undefined"))
        self.result_grade = QtWidgets.QLineEdit(_("Undefined"))
        self.result_grade.setReadOnly(True)
        self.result_grade.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.result_grade.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("Grade:")), self.result_grade)

        group_box.setLayout(group_box_layout)
