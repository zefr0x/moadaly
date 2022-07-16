#!/usr/bin/python3
"""Main file for the GUI."""
import gettext

# import dbus
from PySide6 import QtWidgets, QtGui

from .. import database
from . import result_box
from . import previous_cgpa_box
from . import calculation_system_options_box
from . import grades_panel
from . import manage_profiles_dialogs


# TODO Configure it to use the "/usr/share/locale" directory.
gettext.bindtextdomain("moadaly", "locale")
gettext.textdomain("moadaly")
_ = gettext.gettext


class MainWindow(QtWidgets.QMainWindow):
    """Main window."""

    def __init__(self):
        """Initialize main components of the window."""
        super().__init__()

        self.setMinimumSize(1250, 750)
        self.setWindowTitle(_("Moadaly"))

        main_window_layout = QtWidgets.QVBoxLayout()

        top_panel_layout = QtWidgets.QHBoxLayout()
        bottom_panel_layout = QtWidgets.QVBoxLayout()

        # Create main window widgets.
        self.result_box = result_box.ResultBox()
        self.previous_gpa_box = previous_cgpa_box.PreviousCGPABox()
        self.calculation_system_box = (
            calculation_system_options_box.CalculationSystemBox()
        )
        self.grades_panel = grades_panel.GradesPanel()

        # Add main components to the main window layout.
        top_panel_layout.addWidget(self.result_box)
        top_panel_layout.addWidget(self.previous_gpa_box)
        top_panel_layout.addWidget(self.calculation_system_box)
        bottom_panel_layout.addWidget(self.grades_panel.scroll_area)

        main_window_layout.addLayout(top_panel_layout)
        main_window_layout.addLayout(bottom_panel_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_window_layout)

        self.setCentralWidget(central_widget)

        self.create_menu_bar()

    def create_menu_bar(self):
        """Create all the menu bar components and actions."""
        self.menu_bar = self.menuBar()

        profile_menu = self.menu_bar.addMenu(_("&Profile"))

        # Menu to switch to another profile.
        change_profile_menu = QtWidgets.QMenu(_("&Change Profile"), self)
        change_profile_menu.setIcon(QtGui.QIcon().fromTheme("system-switch-user"))
        # TODO Add action for every available profile in the database.
        profile_menu.addMenu(change_profile_menu)

        # Action to create new profile.
        new_profile_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("contact-new-symbolic"), _("&New Profile"), self
        )
        new_profile_action.setShortcut("Ctrl+N")
        new_profile_action.triggered.connect(self.create_new_profile)
        profile_menu.addAction(new_profile_action)

        delete_current_profile_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("delete"), _("&Delete Current Profile"), self
        )
        delete_current_profile_action.setShortcut("Ctrl+D")
        delete_current_profile_action.triggered.connect(self.delete_profile)
        profile_menu.addAction(delete_current_profile_action)

        # Action to exit the application.
        exit_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("application-exit"), _("&Exit Application"), self
        )
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QtWidgets.QApplication.instance().quit)
        profile_menu.addAction(exit_action)

        tools_menu = self.menu_bar.addMenu(_("&Tools"))
        # TODO Add action for every sub-tool in the application, after creating them.

        about_menu = self.menu_bar.addMenu(_("&About"))
        # TODO Add some information and help links.

    def create_new_profile(self) -> None:
        """Show profile creator dialog."""
        new_profile_dialog = manage_profiles_dialogs.NewProfileDialog(self)

        if new_profile_dialog.exec():
            # TODO Reset the UI for the new profile (May be implemented in another file).
            ...

    def delete_profile(self) -> None:
        """Show a warning message, then delete the profile from the database."""
        confirm_dialog = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Warning,
            _("Delete Current Profile | Moadaly"),
            # TODO Display the name of the current profile.
            _("Are you sure that you want to delete <b>%s</b> profile?"),
            buttons=QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )
        confirm_dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        # TODO Display the name of the current profile.
        confirm_dialog.setInformativeText(
            _(
                "That will permanently delete any semesters and classes under <b>%s</b> profile, "
                + "and any related data."
            )
        )

        if confirm_dialog.exec() == QtWidgets.QMessageBox.Yes:
            # TODO Delete the profile from the database after implementing it.
            # TODO Reset the UI and show another profile.
            ...


def main() -> None:
    """Launch the UI with no arguments."""
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
