"""Where you can specify an old GPA to be added to the calculation."""
from gettext import gettext as _

from PySide6 import QtWidgets


class PreviousGPABox(QtWidgets.QWidget):
    """A Group Box where you can specify a previous GPA, to add it to the calculation."""

    def __init__(self):
        """Initialize components of the previous GPA widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Previous GPA"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QFormLayout()

        # Previous Hours.
        self.previous_hours = QtWidgets.QSpinBox()
        self.previous_hours.setMaximum(100000)
        group_box_layout.addRow(
            QtWidgets.QLabel(_("Previous Hours:")), self.previous_hours
        )

        # Previous GPA.
        self.previous_gpa = QtWidgets.QDoubleSpinBox()
        self.previous_gpa.setSingleStep(0.1)
        # TODO Set the maximum value to 4 or 5 for the GPA depending on the used GPA system.
        self.previous_gpa.setMaximum(5.0)
        group_box_layout.addRow(QtWidgets.QLabel(_("Previous GPA:")), self.previous_gpa)

        group_box.setLayout(group_box_layout)
