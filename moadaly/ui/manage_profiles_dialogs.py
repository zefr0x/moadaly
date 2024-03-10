"""A dialogs for managing the profiles in the database."""

from gettext import gettext as _
from random import randint
from uuid import uuid4

from PySide6 import QtCore, QtGui, QtWidgets


class NewProfileDialog(QtWidgets.QDialog):
    """A dialog to create new profile."""

    new_profile_creation = QtCore.Signal(str, str, str)

    def __init__(self) -> None:
        """Initialize main components of the dialog."""
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()
        layout.addLayout(form_layout)

        self.profile_name = QtWidgets.QLineEdit()
        form_layout.addRow(QtWidgets.QLabel(_("Profile Name")), self.profile_name)

        self.choose_color_button = ProfileColorButton()
        form_layout.addRow(
            QtWidgets.QLabel(_("Profile Color")),
            self.choose_color_button,
        )

        self.profile_id: str = uuid4().hex
        form_layout.addRow(
            QtWidgets.QLabel(_("Profile ID")),
            QtWidgets.QLabel(self.profile_id),
        )

        buttons_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(buttons_layout)

        create_profile_button = QtWidgets.QPushButton(_("Create Profile"))
        create_profile_button.clicked.connect(self.create_profile)
        buttons_layout.addWidget(create_profile_button)

        cancel_operation_button = QtWidgets.QPushButton(_("Cancel"))
        cancel_operation_button.clicked.connect(self.cancel_operation)
        buttons_layout.addWidget(cancel_operation_button)

    def create_profile(self) -> None:
        """Add the new profile to the database."""
        self.new_profile_creation.emit(
            self.profile_id,
            self.profile_name.text(),
            self.choose_color_button.color().name(),
        )
        self.done(1)

    def cancel_operation(self) -> None:
        """Close the dialog without doing any thing."""
        self.done(0)


class ProfileColorButton(QtWidgets.QPushButton):
    """
    Custom QPushButton widget to choose a color and display it.

    Left-clicking the button shows the QColorDialog, while
    right-clicking resets the color to the default.

    Derivative from:
        https://www.pythonguis.com/widgets/qcolorbutton-a-color-selector-tool-for-pyqt/
    """

    def __init__(self) -> None:
        """Set default attributes."""
        super().__init__()

        # Give the button an ID to identify it when changing it's color.
        self.setObjectName("color_button")
        self._color = None

        # Create a random default color.
        self._default = QtGui.QColor().fromRgb(
            randint(0, 255),  # noqa: S311
            randint(0, 255),  # noqa: S311
            randint(0, 255),  # noqa: S311
        )
        self.pressed.connect(self._get_color)

        # Set the default color.
        self.set_color(self._default)

    def set_color(self, color: QtGui.QColor) -> None:
        """When a color is selected, the button color will be changed."""
        if color != self._color:
            self._color = color

        if self._color:
            self.setStyleSheet(
                """QPushButton#color_button {
                    background-color: rgba(%d, %d, %d, %d);
                    border: none;
                    }
                    """
                % self._color.getRgb(),
            )
        else:
            self.setStyleSheet("")

    def color(self) -> QtGui.QColor:
        """Return the current selected color."""
        return self._color

    def _get_color(self) -> None:
        """Show color-picker dialog to select a color."""
        color_dialog = QtWidgets.QColorDialog(self)

        if self._color:
            color_dialog.setCurrentColor(self._color)

        if color_dialog.exec():
            self.set_color(color_dialog.currentColor())

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:  # noqa: N802
        """Handle mouse right click."""
        if e.button() == QtCore.Qt.RightButton:
            # Reset the color to default.
            self.set_color(self._default)

        return super().mousePressEvent(e)
