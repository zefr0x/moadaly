#!/usr/bin/python3
"""Main file for the GUI."""
import gettext
from html import escape as html_escape

# import dbus
from PySide6 import QtWidgets, QtGui

from ..database import Database
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

        self.database = Database()

        main_window_layout = QtWidgets.QVBoxLayout()

        top_panel_layout = QtWidgets.QHBoxLayout()
        bottom_panel_layout = QtWidgets.QVBoxLayout()

        # Create main window widgets.
        self.result_box = result_box.ResultBox()
        self.previous_cgpa_box = previous_cgpa_box.PreviousCGPABox()
        self.calculation_system_box = (
            calculation_system_options_box.CalculationSystemBox()
        )
        self.grades_panel = grades_panel.GradesPanel()

        # Listen to signals when the calculation is updated.
        self.grades_panel.panel_calculation_changed.connect(self.update_results)
        self.previous_cgpa_box.previous_points_changed.connect(self.update_results)

        # Add main components to the main window layout.
        top_panel_layout.addWidget(self.result_box)
        top_panel_layout.addWidget(self.previous_cgpa_box)
        top_panel_layout.addWidget(self.calculation_system_box)
        bottom_panel_layout.addWidget(self.grades_panel.scroll_area)

        main_window_layout.addLayout(top_panel_layout)
        main_window_layout.addLayout(bottom_panel_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_window_layout)

        self.setCentralWidget(central_widget)

        self.create_menu_bar()

        self.load_data()

    def update_results(self):
        """Update the results in the result widget."""
        # Get the results from the grades panel and the previous gpa widget.
        self.result_box.display_new_calculation(
            self.grades_panel.total_points
            + self.previous_cgpa_box.previous_points.value(),
            self.grades_panel.total_credits
            + self.previous_cgpa_box.previous_credit.value(),
        )

    def load_data(self) -> None:
        """
        Load data from the database then push them to the UI.

        It will run after starting the app, when switching profiles and deleting or creating them.
        """
        self.current_profile_data = self.database.get_current_profile_data()

        # Delete all the actions in the "change profile" menu.
        for action in self.change_profile_menu.actions():
            action.deleteLater()

        # Add every available profiles to the "change profile" menu as an action.
        # Exclude the first item, which is the current profile.
        for profile in self.database.get_profiles_list()[1:]:
            # Create a pixmap with the profile color, to be used as an icon.
            pixmap = QtGui.QPixmap(16, 16)
            # No need for converting to QtGui.QColor; "fill" method accepts hex RBG color string.
            pixmap.fill(profile.color)

            select_profile_action = QtGui.QAction(
                QtGui.QIcon(pixmap), profile.name, self
            )
            select_profile_action.triggered.connect(
                lambda checked=None, _id=profile.id: self.database.update_profile_selected_time(
                    _id
                )
            )
            select_profile_action.triggered.connect(self.load_data)

            self.change_profile_menu.addAction(select_profile_action)

        # Fill the calculation system settings.
        if self.current_profile_data.point_scale is None:
            self.calculation_system_box.radio_five_scale_system.setChecked(True)
        else:
            self.calculation_system_box.radio_four_scale_system.setChecked(True)

        if self.current_profile_data.grading_system is None:
            self.calculation_system_box.radio_normal_grading_system.setChecked(True)
        else:
            self.calculation_system_box.radio_curve_grading_system.setChecked(True)

        if self.current_profile_data.score_scale is None:
            self.calculation_system_box.radio_hundred_score_scale.setChecked(True)
        else:
            self.calculation_system_box.radio_ten_score_scale.setChecked(True)

        # TODO Reset the grades panel UI then push new data (May be implemented in another file).

    def create_menu_bar(self):
        """Create all the menu bar components and actions."""
        self.menu_bar = self.menuBar()

        profile_menu = self.menu_bar.addMenu(_("&Profile"))

        # Menu to switch to another profile.
        self.change_profile_menu = QtWidgets.QMenu(_("&Change Profile"), self)
        self.change_profile_menu.setIcon(QtGui.QIcon().fromTheme("system-switch-user"))

        profile_menu.addMenu(self.change_profile_menu)

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
        new_profile_dialog = manage_profiles_dialogs.NewProfileDialog()

        new_profile_dialog.new_profile_creation.connect(
            self.database.create_new_profile
        )

        if new_profile_dialog.exec():
            self.load_data()

    def delete_profile(self) -> None:
        """Show a warning message, then delete the profile from the database."""
        confirm_dialog = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Warning,
            _("Delete Current Profile | Moadaly"),
            _("Are you sure that you want to delete <b>%s</b> profile?")
            % html_escape(self.current_profile_data.name),
            buttons=QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )
        confirm_dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        confirm_dialog.setInformativeText(
            _(
                "That will permanently delete any semesters and classes under <b>%s</b> profile, "
                + "and any related data."
            )
            % html_escape(self.current_profile_data.name)
        )

        if confirm_dialog.exec() == QtWidgets.QMessageBox.Yes:
            self.database.delete_profile(self.current_profile_data.id)
            self.load_data()


def main() -> None:
    """Launch the UI with no arguments."""
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
