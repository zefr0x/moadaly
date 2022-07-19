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
        group_box_layout.addWidget(self.init_score_scale_box())

        main_group_box.setLayout(group_box_layout)

    def init_point_scale_box(self) -> QtWidgets.QGroupBox:
        """Create point scale setting box."""
        point_scale_group_box = QtWidgets.QGroupBox(_("Point Scale"))
        point_scale_group_box_layout = QtWidgets.QVBoxLayout()

        self.radio_five_scale_system = QtWidgets.QRadioButton("5.000")

        self.radio_four_scale_system = QtWidgets.QRadioButton("4.000")
        # TODO Enable the option when the 4 point scale system is implemented.
        self.radio_four_scale_system.setDisabled(True)

        for widget in (self.radio_five_scale_system, self.radio_four_scale_system):
            point_scale_group_box_layout.addWidget(widget)

        point_scale_group_box.setLayout(point_scale_group_box_layout)

        return point_scale_group_box

    def init_grading_system_box(self) -> QtWidgets.QGroupBox:
        """Create grading system setting box."""
        point_scale_group_box = QtWidgets.QGroupBox(_("Grading System"))
        point_scale_group_box_layout = QtWidgets.QVBoxLayout()

        self.radio_normal_grading_system = QtWidgets.QRadioButton(_("Normal"))

        self.radio_curve_grading_system = QtWidgets.QRadioButton(_("Curve"))
        # TODO Enable the option when the curve grading system is implemented.
        self.radio_curve_grading_system.setDisabled(True)

        for widget in (
            self.radio_normal_grading_system,
            self.radio_curve_grading_system,
        ):
            point_scale_group_box_layout.addWidget(widget)

        point_scale_group_box.setLayout(point_scale_group_box_layout)

        return point_scale_group_box

    def init_score_scale_box(self) -> QtWidgets.QGroupBox:
        """Create score scale setting box."""
        score_scale_group_box = QtWidgets.QGroupBox(_("Score Scale"))
        score_scale_group_box_layout = QtWidgets.QVBoxLayout()

        self.radio_hundred_score_scale = QtWidgets.QRadioButton("100")

        self.radio_ten_score_scale = QtWidgets.QRadioButton("10")
        # Enable it when the ten score scale get implemented.
        self.radio_ten_score_scale.setDisabled(True)

        for widget in (self.radio_hundred_score_scale, self.radio_ten_score_scale):
            score_scale_group_box_layout.addWidget(widget)

        score_scale_group_box.setLayout(score_scale_group_box_layout)

        return score_scale_group_box
