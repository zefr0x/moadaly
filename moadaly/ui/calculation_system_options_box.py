"""Some option for the used calculation system."""
from gettext import gettext as _

from PySide6 import QtWidgets


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
