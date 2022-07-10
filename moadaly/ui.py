#!/usr/bin/python3
"""Main file for the GUI."""
import gettext
from uuid import uuid1

# import dbus
from PySide6 import QtCore, QtWidgets, QtGui

from . import database


# TODO Configure it to use the "/usr/share/locale" directory.
gettext.bindtextdomain("moadaly", "locale")
gettext.textdomain("moadaly")
_ = gettext.gettext


class MainWindow(QtWidgets.QMainWindow):
    """Main window."""

    def __init__(self):
        """Initialize main components of the window."""
        super().__init__()

        self.setMinimumSize(1000, 750)
        self.setWindowTitle(_("Moadaly"))

        main_window_layout = QtWidgets.QVBoxLayout()

        top_panel_layout = QtWidgets.QHBoxLayout()
        bottom_panel_layout = QtWidgets.QVBoxLayout()

        # Create main window widgets.
        self.result_box = ResultBox()
        self.previous_gpa_box = PreviousGPABox()
        self.calculation_system_box = CalculationSystemBox()
        self.grades_panel = GradesPanel()

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


class ResultBox(QtWidgets.QWidget):
    """A Group Box where the results are displayed, such as, GPA, grade, total hours and points."""

    def __init__(self):
        """Initialize components of the results widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Result"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QFormLayout()

        # Result GPA.
        self.result_gpa = QtWidgets.QLabel(_("Undefined"))
        self.result_gpa.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("GPA:")), self.result_gpa)

        # Result hours.
        self.result_hours = QtWidgets.QLabel("0")
        self.result_hours.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("Hours:")), self.result_hours)

        # Result points.
        self.result_points = QtWidgets.QLabel("0.00")
        self.result_points.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("Points:")), self.result_points)

        # Result grade.
        self.result_grade = QtWidgets.QLabel(_("Undefined"))
        self.result_grade.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addRow(QtWidgets.QLabel(_("Grade:")), self.result_grade)

        group_box.setLayout(group_box_layout)


class PreviousGPABox(QtWidgets.QWidget):
    """A Group Box where you can specify a previous GPA, to add it to the calculation."""

    def __init__(self):
        """Initialize components of the previous GPA widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Previous GPA"))
        group_box.setParent(self)

        group_box_layout = QtWidgets.QFormLayout()

        # Previous Hours.
        self.previous_hours = QtWidgets.QLineEdit()
        self.previous_hours.setValidator(QtGui.QIntValidator(bottom=0))
        group_box_layout.addRow(
            QtWidgets.QLabel(_("Previous Hours:")), self.previous_hours
        )

        # Previous GPA.
        self.previous_gpa = QtWidgets.QLineEdit()
        # TODO Set the maximum value to 4 or 5 for the GPA depending on the used GPA system.
        self.previous_gpa.setValidator(QtGui.QDoubleValidator(bottom=0))
        group_box_layout.addRow(QtWidgets.QLabel(_("Previous GPA:")), self.previous_gpa)

        group_box.setLayout(group_box_layout)


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


class GradesPanel(QtWidgets.QWidget):
    """A panel to display semesters, and to handle the addition of new semesters."""

    def __init__(self):
        """Initialize base components of the panel."""
        super().__init__()

        self.semesters = []

        self.layout = QtWidgets.QVBoxLayout(self)

        self.scroll_area = QtWidgets.QScrollArea()

        add_semester_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("list-add"), _("New Semester")
        )
        add_semester_button.setStyleSheet("background-color: green;")
        add_semester_button.setFixedWidth(200)
        add_semester_button.clicked.connect(self.add_new_semester)
        self.layout.addWidget(add_semester_button, alignment=QtCore.Qt.AlignCenter)

        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        # FIXME Scroll area doesn't cover all the available space in the window.
        self.scroll_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.scroll_area.setFixedHeight(500)
        self.scroll_area.setWidget(self)

    def add_new_semester(self):
        """Add new semester widget to the grades panel."""
        widget = SemesterWidget(self)
        self.semesters.append(widget)
        self.layout.insertWidget(len(self.semesters) - 1, widget)


class SemesterWidget(QtWidgets.QWidget):
    """A semester that contain a list of corses, to be added to the grades panel."""

    def __init__(self, parent_panel):
        """Initialize a new semester and it's base components."""
        super().__init__()

        self.parent_panel = parent_panel
        self.semester_id = uuid1()
        self.courses = []

        self.layout = QtWidgets.QVBoxLayout(self)

        # Create the semester title bar.
        title_layout = QtWidgets.QHBoxLayout()

        self.title = QtWidgets.QLabel(
            _("Semester %d") % (len(self.parent_panel.semesters) + 1)
        )
        self.title.setStyleSheet(
            """
        font: bold;
        font-size: 25px;
        background-color: green;
        """
        )
        self.title.setFixedHeight(30)
        title_layout.addWidget(self.title)

        delete_semester_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("delete"), ""
        )
        delete_semester_button.setFixedWidth(80)
        delete_semester_button.clicked.connect(self.delete_semester)
        title_layout.addWidget(delete_semester_button)

        self.layout.addLayout(title_layout)

        # Create the header for the corses.
        # TODO Use a better alignment method if possible.
        name_header = QtWidgets.QLabel(_("Course Name"))
        name_header.setContentsMargins(140, 0, 0, 0)
        score_header = QtWidgets.QLabel(_("Score"))
        score_header.setContentsMargins(150, 0, 0, 0)
        hours_header = QtWidgets.QLabel(_("Hours"))
        hours_header.setContentsMargins(155, 0, 0, 0)
        grade_header = QtWidgets.QLabel(_("Grade"))
        grade_header.setContentsMargins(110, 0, 0, 0)

        headers_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(headers_layout)
        for header in [
            name_header,
            score_header,
            hours_header,
            grade_header,
        ]:
            headers_layout.addWidget(header)

        # Create a button to add a now course.
        add_course_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("list-add"), ""
        )
        add_course_button.setStyleSheet("background-color: green;")
        add_course_button.setFixedWidth(80)
        add_course_button.clicked.connect(self.add_new_course)
        self.layout.addWidget(add_course_button)

    def delete_semester(self):
        """Remove a specified semester from the grades panel."""
        semester_index = self.parent_panel.semesters.index(self)
        self.parent_panel.semesters.pop(semester_index)
        self.deleteLater()

        for i in range(semester_index, len(self.parent_panel.semesters)):
            self.parent_panel.semesters[i].title.setText(_("Semester %d") % (i + 1))

    def add_new_course(self):
        """Add new course widget to the semester."""
        widget = CourseWidget(self)
        self.courses.append(widget)
        self.layout.insertWidget(len(self.courses) + 1, widget)


class CourseWidget(QtWidgets.QWidget):
    """A course that can be added inside a semester."""

    def __init__(self, parent_semester):
        """Initialize a new course and it's components."""
        super().__init__()

        self.course_id = uuid1()
        self.parent_semester = parent_semester

        self.layout = QtWidgets.QHBoxLayout(self)

        self.title = QtWidgets.QLabel(
            _("Course %d:") % (len(self.parent_semester.courses) + 1)
        )
        self.title.setStyleSheet(
            """
        font-size: 12px;
        """
        )
        self.layout.addWidget(self.title)

        self.name = QtWidgets.QLineEdit()
        self.layout.addWidget(self.name)

        self.score = QtWidgets.QLineEdit()
        # FIXME Validator accepts numbers between 100 and 1000.
        self.score.setValidator(
            QtGui.QDoubleValidator(
                0.0, 100.0, 2, notation=QtGui.QDoubleValidator.StandardNotation
            )
        )
        self.score.textChanged.connect(self.score_changed)
        self.layout.addWidget(self.score)

        self.hours = QtWidgets.QLineEdit()
        self.hours.setValidator(QtGui.QIntValidator(bottom=0))
        self.layout.addWidget(self.hours)

        self.grade = QtWidgets.QComboBox()
        self.grade.addItems(
            [
                _("Undefined"),
                _("A+"),
                _("A"),
                _("B+"),
                _("B"),
                _("C+"),
                _("C"),
                _("D+"),
                _("D"),
                _("F"),
            ]
        )
        self.grade.currentIndexChanged.connect(self.grade_changed)
        self.layout.addWidget(self.grade)

        # TODO Add points field after the grade field.

        self.delete_course_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("delete"), ""
        )
        self.delete_course_button.clicked.connect(self.delete_course)
        self.layout.addWidget(self.delete_course_button)

    def score_changed(self) -> None:
        """Change the grade when the score is changed."""
        try:
            self.grade.setCurrentIndex(get_grade_from_score(float(self.score.text())))
        except ValueError:
            # When we have empty string, set it to index zero (Undefined).
            self.grade.setCurrentIndex(0)

    def grade_changed(self) -> None:
        """Change the score when the grade is changed."""
        try:
            score_value = float(self.score.text())
        except ValueError:
            # When we have empty string.
            score_value = 0.0

        if (
            self.grade.currentIndex() != get_grade_from_score(score_value)
            and self.grade.currentIndex() != 0
        ):
            self.score.setText(str(get_score_from_grade(self.grade.currentIndex())))

    def delete_course(self):
        """Remove a specified course from the semester."""
        course_index = self.parent_semester.courses.index(self)
        self.parent_semester.courses.pop(course_index)
        self.deleteLater()

        for i in range(course_index, len(self.parent_semester.courses)):
            self.parent_semester.courses[i].title.setText(_("Course %d") % (i + 1))


def get_grade_from_score(score: float) -> int:
    """Convert the score to a number that refers to the grade."""
    if 100 >= score >= 95:
        return 1
    elif score >= 90:
        return 2
    elif score >= 85:
        return 3
    elif score >= 80:
        return 4
    elif score >= 75:
        return 5
    elif score >= 70:
        return 6
    elif score >= 65:
        return 7
    elif score >= 60:
        return 8
    else:
        return 9


def get_score_from_grade(grade: int) -> int:
    """Convert the number that refers to the grade to a score."""
    if grade == 1:
        return 95
    elif grade == 2:
        return 90
    elif grade == 3:
        return 85
    elif grade == 4:
        return 80
    elif grade == 5:
        return 75
    elif grade == 6:
        return 70
    elif grade == 7:
        return 65
    elif grade == 8:
        return 60
    else:
        return 0

def main() -> None:
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
