"""Tool to covert score to grade."""
from typing import Union
from gettext import gettext as _

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui

from ... import common_conversions


class GradeCalculator(QtWidgets.QDialog):
    """A tool widget for calculating grade from score."""

    tool_name = _("Grade Calculator")
    # TODO Add icon.
    tool_icon = ""

    def __init__(self):
        """Initialize main components."""
        super().__init__()

        self.setWindowTitle(_("Grade Calculator | Moadaly"))

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        form_layout = QtWidgets.QFormLayout()
        main_layout.addLayout(form_layout)

        self.score = QtWidgets.QDoubleSpinBox()
        self.score.setRange(0.0, 100.0)
        self.score.setSingleStep(0.25)
        self.score.valueChanged.connect(self.score_updated)
        form_layout.addRow(QtWidgets.QLabel(_("Score")), self.score)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(60, 100)
        self.slider.setTickInterval(5)
        self.slider.valueChanged.connect(self.score_updated)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        # TODO Add some stylesheet for some fancy gradient.
        main_layout.addWidget(self.slider)

        self.grade = QtWidgets.QLineEdit("Undefined")
        self.grade.setAlignment(QtCore.Qt.AlignCenter)
        self.grade.setReadOnly(True)
        self.grade.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.grade.font()

        # Set grade initial colors.
        grade_palette = QtGui.QPalette()
        grade_palette.setColor(
            QtGui.QPalette.Base, QtGui.QColor(common_conversions.grades_colors[0])
        )
        grade_palette.setColor(QtGui.QPalette.Text, QtGui.QColor("black"))
        self.grade.setPalette(grade_palette)

        # Set grade font.
        grade_font = QtGui.QFont()
        grade_font.setBold(True)
        self.grade.setFont(grade_font)

        main_layout.addWidget(self.grade)

    def score_updated(self, score: Union[int, float]) -> None:
        """When score or slider updated, update grade and slider or score."""
        if type(score) is int:
            self.score.setValue(score)
        else:
            self.slider.setValue(int(score))
        grade_index = common_conversions.get_grade_from_score(score)

        self.grade.setText(common_conversions.grades[grade_index])

        # Change grade background
        grade_palette = self.grade.palette()
        grade_palette.setColor(
            QtGui.QPalette.Base,
            QtGui.QColor(common_conversions.grades_colors[grade_index]),
        )
        self.grade.setPalette(grade_palette)

    @classmethod
    def exec_tool(cls) -> None:
        """Show the tool dialog window."""
        cls().exec()
