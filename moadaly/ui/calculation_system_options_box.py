"""Some option for the used calculation system."""
from gettext import gettext as _

from PySide6 import QtCore
from PySide6 import QtWidgets


class CalculationSystemBox(QtWidgets.QWidget):
    """A Group Box where you can specify the GPA calculation system."""

    def __init__(self) -> None:
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
