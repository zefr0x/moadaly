"""Main file for the GUI."""

import gettext
from html import escape as html_escape
from typing import Sequence
from webbrowser import open as open_url

from PySide6 import QtCore, QtGui, QtWidgets

from moadaly.__about__ import APP_ID, BUG_REPORT_URL, PROJECT_HOME_PAGE_URL
from moadaly.database import Database
from moadaly.ui import (
    calculation_system_options_box,
    grades_panel,
    help_dialogs,
    manage_profiles_dialogs,
    previous_cgpa_box,
    result_box,
)
from moadaly.ui.extra_tools import extra_tools_classes

# TODO: Configure it to use the "/usr/share/locale" directory.
gettext.bindtextdomain("moadaly", "locale")
gettext.textdomain("moadaly")
_ = gettext.gettext


class MainWindow(QtWidgets.QMainWindow):
    """Main window."""

    window_resized = QtCore.Signal(tuple)

    def __init__(self) -> None:
        """Initialize main components of the window."""
        super().__init__()

        # FIX: Use a smaller window minimum size.
        self.setMinimumSize(1250, 1000)
        self.setWindowTitle(_("Moadaly"))
        self.setWindowIcon(QtGui.QIcon.fromTheme(APP_ID))

        self.database = Database()

        main_window_layout = QtWidgets.QVBoxLayout()

        top_panel_layout = QtWidgets.QHBoxLayout()
        self.bottom_panel_layout = QtWidgets.QVBoxLayout()

        # Create main window widgets.
        self.result_box = result_box.ResultBox()
        self.previous_cgpa_box = previous_cgpa_box.PreviousCGPABox()
        self.calculation_system_box = (
            calculation_system_options_box.CalculationSystemBox()
        )

        # Listen to signal from previous cgpa widget.
        self.previous_cgpa_box.previous_points_changed.connect(self.update_results)

        # Listen to signals from calculation system box
        self.calculation_system_box.point_scale_button_group.buttonClicked.connect(
            self.apply_point_scale_config,
        )

        # Add main components to the main window layout.
        top_panel_layout.addStretch(1)
        top_panel_layout.addWidget(self.result_box, 4)
        top_panel_layout.addStretch(1)
        top_panel_layout.addWidget(self.previous_cgpa_box, 4)
        top_panel_layout.addStretch(1)
        top_panel_layout.addWidget(self.calculation_system_box, 4)
        top_panel_layout.addStretch(1)

        main_window_layout.addLayout(top_panel_layout, 2)
        main_window_layout.addStretch(1)
        main_window_layout.addLayout(self.bottom_panel_layout, 3)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_window_layout)

        self.setCentralWidget(central_widget)

        self.create_menu_bar()

        self.load_data()

    def update_results(self) -> None:
        """Update the results in the result widget."""
        # Get the results from the grades panel and the previous gpa widget.
        self.grades_panel: grades_panel.GradesPanel

        self.result_box.display_new_calculation(
            self.grades_panel.total_points
            + self.previous_cgpa_box.previous_points.value(),
            self.grades_panel.total_credits
            + self.previous_cgpa_box.previous_credit.value(),
        )

    def load_data(self) -> None:
        """
        Load data from the database then push them to the UI.

        It will run after starting the app,
        when switching profiles and deleting or creating them.
        """
        self.current_profile_data = self.database.get_current_profile_data()

        # Delete all the actions in the "change profile" menu.
        for action in self.change_profile_menu.actions():
            action.deleteLater()

        # Add every available profiles to the "change profile" menu as an action.
        # Exclude the first item, which is the current profile.
        for profile in self.database.get_profiles_data():
            # Create a pixmap with the profile color, to be used as an icon.
            pixmap = QtGui.QPixmap(16, 16)
            # No need for converting to QtGui.QColor; it accepts hex RBG color string.
            pixmap.fill(profile.color)

            select_profile_action = QtGui.QAction(
                QtGui.QIcon(pixmap),
                profile.name,
                self,
            )
            select_profile_action.triggered.connect(
                lambda _checked=None,
                _id=profile.id: self.database.update_profile_selected_time(_id),
            )
            select_profile_action.triggered.connect(self.load_data)

            if profile.id == self.current_profile_data.id:
                select_profile_action.setDisabled(True)

            self.change_profile_menu.addAction(select_profile_action)

        # Fill the calculation system settings.
        self.calculation_system_box.point_scale_button_group.button(
            self.current_profile_data.point_scale,
        ).setChecked(True)

        # Apply settings in result box
        self.result_box.point_scale = self.current_profile_data.point_scale

        if hasattr(self, "grades_panel"):
            # If there is a grades panel, delete it.
            self.grades_panel.scroll_area.deleteLater()
            self.grades_panel.deleteLater()
            del self.grades_panel
        else:
            # Apply settings in previous CGPA box, only when data first loaded.
            # Updating the max when changing the point scale is via another function.
            self.previous_cgpa_box.previous_cgpa.setMaximum(
                self.current_profile_data.point_scale,
            )

        # Create new grades panel.
        self.grades_panel = grades_panel.GradesPanel(
            self.current_profile_data.id,
            self.current_profile_data.point_scale,
        )
        # Set the size of the scroll area.
        # It will be updated also every time you change the window's size.
        self.grades_panel.resize_scroll_area(self.size().toTuple())
        self.bottom_panel_layout.addWidget(self.grades_panel.scroll_area)

        # Call function when the main widndow got resized to resize the scroll area.
        self.window_resized.connect(self.grades_panel.resize_scroll_area)

        # Listen to the grades panel signals.
        self.grades_panel.panel_calculation_changed.connect(self.update_results)
        self.grades_panel.semester_created.connect(self.database.create_new_semester)
        self.grades_panel.semester_deleted.connect(self.database.delete_semester)
        self.grades_panel.course_created.connect(self.database.create_new_course)
        self.grades_panel.course_deleted.connect(self.database.delete_course)
        self.grades_panel.course_name_updated.connect(self.database.update_course_name)
        self.grades_panel.course_score_updated.connect(
            self.database.update_course_score,
        )
        self.grades_panel.course_credits_updated.connect(
            self.database.update_course_credit_units,
        )

        for semester_id, courses_data in self.database.get_courses_data(
            self.current_profile_data.id,
        ).items():
            self.grades_panel.add_new_semester(semester_id)
            for course_data in courses_data:
                self.grades_panel.semesters[-1].add_new_course(
                    course_data.id,
                    course_data.name,
                    course_data.score,
                    course_data.credit_units,
                )

        # Close the database, since function used here don't close it.
        self.database.close()

    def create_menu_bar(self) -> None:
        """Create all the menu bar components and actions."""
        self.menu_bar = self.menuBar()

        profile_menu = self.menu_bar.addMenu(_("&Profile"))

        # Menu to switch to another profile.
        self.change_profile_menu = QtWidgets.QMenu(_("&Change Profile"), self)
        self.change_profile_menu.setIcon(
            QtGui.QIcon().fromTheme("system-switch-user-symbolic"),
        )

        profile_menu.addMenu(self.change_profile_menu)

        # Action to create new profile.
        new_profile_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("contact-new-symbolic"),
            _("&New Profile"),
            self,
        )
        new_profile_action.setShortcut("Ctrl+N")
        new_profile_action.triggered.connect(self.create_new_profile)
        profile_menu.addAction(new_profile_action)

        # Action to delete current profile.
        delete_current_profile_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("delete"),
            _("&Delete Current Profile"),
            self,
        )
        delete_current_profile_action.setShortcut("Ctrl+D")
        delete_current_profile_action.triggered.connect(self.delete_profile)
        profile_menu.addAction(delete_current_profile_action)

        # Action to export database.
        export_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("document-export"),
            _("&Export Data"),
            self,
        )
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_data_file)
        profile_menu.addAction(export_action)

        # Action to import to database.
        import_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("document-import"),
            _("&Import Data"),
            self,
        )
        import_action.setShortcut("Ctrl+I")
        # import_action.triggered.connect()  # noqa: ERA001
        # TODO: Enable when the import functionality get implemented.
        import_action.setDisabled(True)
        profile_menu.addAction(import_action)

        # Action to exit the application.
        exit_action = QtGui.QAction(
            QtGui.QIcon().fromTheme("application-exit"),
            _("E&xit Application"),
            self,
        )
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QtWidgets.QApplication.instance().quit)
        profile_menu.addAction(exit_action)

        tools_menu = self.menu_bar.addMenu(_("&Tools"))
        for tool in extra_tools_classes:
            action = QtGui.QAction(
                QtGui.QIcon.fromTheme(tool.tool_icon),
                tool.tool_name,
                self,
            )
            action.triggered.connect(tool.exec_tool)
            tools_menu.addAction(action)

        help_menu = self.menu_bar.addMenu(_("&Help"))

        home_page = QtGui.QAction(
            QtGui.QIcon.fromTheme("github-repo"),
            _("&GitHub"),
            self,
        )
        home_page.triggered.connect(lambda: open_url(PROJECT_HOME_PAGE_URL))
        help_menu.addAction(home_page)

        # TODO: Change the icon.
        report_bug = QtGui.QAction(
            QtGui.QIcon.fromTheme("tools-report-bug"),
            _("Report a &Bug"),
            self,
        )
        report_bug.triggered.connect(lambda: open_url(BUG_REPORT_URL))
        help_menu.addAction(report_bug)

        about_qt = QtGui.QAction(QtGui.QIcon.fromTheme("qt"), _("About &Qt"), self)
        about_qt.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(self))
        help_menu.addAction(about_qt)

        about = QtGui.QAction(
            QtGui.QIcon.fromTheme("help-about-symbolic"),
            _("&About Moadaly"),
            self,
        )
        about.triggered.connect(lambda: help_dialogs.About().exec())
        help_menu.addAction(about)

    def create_new_profile(self) -> None:
        """Show profile creator dialog."""
        new_profile_dialog = manage_profiles_dialogs.NewProfileDialog()

        new_profile_dialog.new_profile_creation.connect(
            self.database.create_new_profile,
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
                "That will permanently delete any semesters and classes under "
                "<b>%s</b> profile, and any related data.",
            )
            % html_escape(self.current_profile_data.name),
        )

        if confirm_dialog.exec() == QtWidgets.QMessageBox.Yes:
            self.database.delete_profile(self.current_profile_data.id)
            self.load_data()

    def export_data_file(self) -> None:
        """Get directory from the user then export a json file to it."""
        file_path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Moadaly Data File",
            "~/moadaly_data.json",
            "JSON file (*.json)",
            # options=QtWidgets.QFileDialog.Option.ShowDirsOnly,  # noqa: ERA001
        )[0]

        if file_path:
            self.database.export_to_json(file_path)

    def apply_point_scale_config(
        self,
        _button: QtWidgets.QPushButton,
    ) -> None:
        """Apply changes when changing point scale."""
        new_point_scale: int = (
            self.calculation_system_box.point_scale_button_group.checkedId()
        )

        if new_point_scale != self.current_profile_data.point_scale:
            self.database.change_point_scale(
                self.current_profile_data.id,
                new_point_scale,
            )

            new_previous_cgpa = (
                self.previous_cgpa_box.previous_cgpa.value()
                * new_point_scale
                / self.current_profile_data.point_scale
            )

            self.previous_cgpa_box.previous_cgpa.setMaximum(new_point_scale)

            # Update value of the previous CGPA.
            self.previous_cgpa_box.previous_cgpa.setValue(new_previous_cgpa)

            self.load_data()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # noqa: N802
        """Send a signal when the main window is resized."""
        self.window_resized.emit(event.size().toTuple())


def main_ui(argv: Sequence[str]) -> int:
    """Launch the UI with arguments."""
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    return app.exec()
