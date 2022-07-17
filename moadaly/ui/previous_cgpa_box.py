"""Where you can specify an old CGPA to be added to the calculation."""
from gettext import gettext as _

from PySide6 import QtCore, QtWidgets


class PreviousCGPABox(QtWidgets.QWidget):
    """A Group Box where you can specify a previous CGPA, to add it to the calculation."""

    previous_points_changed = QtCore.Signal()

    def __init__(self):
        """Initialize components of the previous CGPA widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Previous CGPA"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QFormLayout()
        group_box.setLayout(group_box_layout)

        # Previous credit units.
        self.previous_credit = QtWidgets.QSpinBox()
        self.previous_credit.setMaximum(100000)
        self.previous_credit.valueChanged.connect(self.update_previous_points)
        group_box_layout.addRow(
            QtWidgets.QLabel(_("Previous Credit Units")), self.previous_credit
        )

        # Previous CGPA.
        self.previous_cgpa = QtWidgets.QDoubleSpinBox()
        self.previous_cgpa.setDecimals(3)
        self.previous_cgpa.setSingleStep(0.1)
        # TODO Set the maximum value to 4 or 5 for the GPA depending on the used GPA system.
        # TODO Set decimals count to three decimal values.
        self.previous_cgpa.setMaximum(5.0)
        self.previous_cgpa.valueChanged.connect(self.update_previous_points)
        group_box_layout.addRow(
            QtWidgets.QLabel(_("Previous CGPA")), self.previous_cgpa
        )

        # Previous points.
        self.previous_points = QtWidgets.QDoubleSpinBox()
        self.previous_points.setReadOnly(True)
        self.previous_points.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.previous_points.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.previous_points.setMaximum(10000)
        self.previous_points.setDecimals(3)
        group_box_layout.addRow(
            QtWidgets.QLabel(_("Previous Points")), self.previous_points
        )

    def update_previous_points(self) -> None:
        """Update previous points when CGPA or credit is changed."""
        self.previous_points.setValue(
            self.previous_cgpa.value() * self.previous_credit.value()
        )

        self.previous_points_changed.emit()
