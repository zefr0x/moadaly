#!/usr/bin/python3
"""Main file for the GUI."""
import gettext

# import dbus
from PySide6 import QtWidgets, QtGui

from .. import database
from . import result_box
from . import previous_gpa_box
from . import calculation_system_options_box
from . import grades_panel


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
        self.previous_gpa_box = previous_gpa_box.PreviousGPABox()
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
        # TODO Link the action to a dialog to create a new profile in the database.
        profile_menu.addAction(new_profile_action)

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


def main() -> None:
    """Launch the UI with no arguments."""
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
