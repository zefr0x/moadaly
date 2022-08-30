"""The result box where the results are displayed."""
from gettext import gettext as _

from PySide6 import QtCore, QtWidgets

from .. import common_conversions


class ResultBox(QtWidgets.QWidget):
    """A Group Box where the results are displayed, GPA, grade, credits and points."""

    point_scale: int

    def __init__(self):
        """Initialize components of the results widget."""
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(
            QtWidgets.QLabel(_("<h3>Result</h3>")), alignment=QtCore.Qt.AlignCenter
        )

        form_layout = QtWidgets.QFormLayout()
        main_layout.addLayout(form_layout)

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
        form_layout.addRow(QtWidgets.QLabel(_("CGPA")), self.result_gpa)

        # Result hours.
        self.result_credits = QtWidgets.QSpinBox()
        self.result_credits.setReadOnly(True)
        self.result_credits.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.result_credits.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.result_credits.setStyleSheet(
            """
        font: bold;
        """
        )
        form_layout.addRow(QtWidgets.QLabel(_("Credit Units")), self.result_credits)

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
        form_layout.addRow(QtWidgets.QLabel(_("Points")), self.result_points)

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
        form_layout.addRow(QtWidgets.QLabel(_("Grade")), self.result_grade)

        main_layout.addStretch()

    def display_new_calculation(self, points, credits) -> None:
        """Display the new results."""
        if credits:
            cgpa = points / credits
            self.result_gpa.setValue(cgpa)
            self.result_credits.setValue(credits)
            self.result_points.setValue(points)
            # FIXME The grade is displayed "A+" while it should be "A"
            # when the points are exactly 4.75 and the credits are 1.
            self.result_grade.setText(
                common_conversions.get_grade_from_gpa(self.point_scale, cgpa)
            )
