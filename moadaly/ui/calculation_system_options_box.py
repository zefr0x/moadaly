"""Some option for the used calculation system."""
from gettext import gettext as _

from PySide6 import QtCore
from PySide6 import QtWidgets


class CalculationSystemBox(QtWidgets.QWidget):
    """A Group Box where you can specify the GPA calculation system."""

    def __init__(self):
        """Initialize components of the calculation system widget."""
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(
            QtWidgets.QLabel(_("<h3>Calculation System</h3>")),
            alignment=QtCore.Qt.AlignCenter,
        )

        content_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(content_layout)

        content_layout.addLayout(self.init_point_scale_box())
        content_layout.addSpacing(30)
        content_layout.addLayout(self.init_grading_system_box())
        content_layout.addSpacing(30)
        content_layout.addLayout(self.init_score_scale_box())

    def init_point_scale_box(self) -> QtWidgets.QGroupBox:
        """Create point scale setting box."""
        point_scale_layout = QtWidgets.QVBoxLayout()

        point_scale_layout.addWidget(QtWidgets.QLabel(_("<h4>Point Scale</h4>")))

        self.point_scale_button_group = QtWidgets.QButtonGroup()

        radio_five_scale_system = QtWidgets.QRadioButton("5.000")
        point_scale_layout.addWidget(radio_five_scale_system)
        self.point_scale_button_group.addButton(radio_five_scale_system, 5)

        radio_four_scale_system = QtWidgets.QRadioButton("4.000")
        point_scale_layout.addWidget(radio_four_scale_system)
        self.point_scale_button_group.addButton(radio_four_scale_system, 4)

        point_scale_layout.addStretch()

        return point_scale_layout

    def init_grading_system_box(self) -> QtWidgets.QGroupBox:
        """Create grading system setting box."""
        grading_system_layout = QtWidgets.QVBoxLayout()

        grading_system_layout.addWidget(QtWidgets.QLabel(_("<h4>Grading System</h4>")))

        self.grading_system_button_group = QtWidgets.QButtonGroup()

        radio_normal_grading_system = QtWidgets.QRadioButton(_("Normal"))
        grading_system_layout.addWidget(radio_normal_grading_system)
        self.grading_system_button_group.addButton(radio_normal_grading_system, 0)

        radio_curve_grading_system = QtWidgets.QRadioButton(_("Curve"))
        grading_system_layout.addWidget(radio_curve_grading_system)
        self.grading_system_button_group.addButton(radio_curve_grading_system, 1)
        # TODO Enable the option when the curve grading system is implemented.
        radio_curve_grading_system.setDisabled(True)

        grading_system_layout.addStretch()

        return grading_system_layout

    def init_score_scale_box(self) -> QtWidgets.QGroupBox:
        """Create score scale setting box."""
        score_scale_group_box = QtWidgets.QGroupBox(_("Score Scale"))

        score_scale_layout = QtWidgets.QVBoxLayout()

        score_scale_layout.addWidget(QtWidgets.QLabel(_("<h4>Score Scale</h4>")))

        self.score_scale_button_group = QtWidgets.QButtonGroup()

        radio_hundred_score_scale = QtWidgets.QRadioButton("100")
        score_scale_layout.addWidget(radio_hundred_score_scale)
        self.score_scale_button_group.addButton(radio_hundred_score_scale, 100)

        radio_ten_score_scale = QtWidgets.QRadioButton("10")
        score_scale_layout.addWidget(radio_ten_score_scale)
        self.score_scale_button_group.addButton(radio_ten_score_scale, 10)
        # Enable it when the ten score scale get implemented.
        radio_ten_score_scale.setDisabled(True)

        score_scale_layout.addStretch()

        return score_scale_layout
