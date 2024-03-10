"""Where you can specify an old CGPA to be added to the calculation."""

from gettext import gettext as _

from PySide6 import QtCore, QtWidgets


# TODO: Save previous CGPA in database.
class PreviousCGPABox(QtWidgets.QWidget):
    """A Group Box for previous CGPA, to be added to the calculation."""

    previous_points_changed = QtCore.Signal()

    def __init__(self) -> None:
        """Initialize components of the previous CGPA widget."""
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(
            QtWidgets.QLabel(_("<h3>Previous CGPA</h3>")),
            alignment=QtCore.Qt.AlignCenter,
        )

        form_layout = QtWidgets.QFormLayout()
        main_layout.addLayout(form_layout, stretch=1)

        # Previous credit units.
        self.previous_credit = QtWidgets.QSpinBox()
        self.previous_credit.setMaximum(100000)
        self.previous_credit.valueChanged.connect(self.update_previous_points)
        form_layout.addRow(
            QtWidgets.QLabel(_("Previous Credit Units")),
            self.previous_credit,
        )

        # Previous CGPA.
        self.previous_cgpa = QtWidgets.QDoubleSpinBox()
        self.previous_cgpa.setDecimals(3)
        self.previous_cgpa.setSingleStep(0.1)
        # The maximum value is being set when loading the data in the main file.
        self.previous_cgpa.valueChanged.connect(self.update_previous_points)
        form_layout.addRow(QtWidgets.QLabel(_("Previous CGPA")), self.previous_cgpa)

        # Previous points.
        self.previous_points = QtWidgets.QDoubleSpinBox()
        self.previous_points.setReadOnly(True)
        self.previous_points.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.previous_points.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.previous_points.setMaximum(10000)
        self.previous_points.setDecimals(3)
        form_layout.addRow(QtWidgets.QLabel(_("Previous Points")), self.previous_points)

    def update_previous_points(self) -> None:
        """Update previous points when CGPA or credit is changed."""
        self.previous_points.setValue(
            self.previous_cgpa.value() * self.previous_credit.value(),
        )

        self.previous_points_changed.emit()
