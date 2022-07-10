"""A Grades panel where you can create semesters, courses and insert the scores."""
from gettext import gettext as _
from uuid import uuid1

from PySide6 import QtCore, QtGui, QtWidgets

from .. import common_conversions


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
            self.grade.setCurrentIndex(
                common_conversions.get_grade_from_score(float(self.score.text()))
            )
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
            self.grade.currentIndex()
            != common_conversions.get_grade_from_score(score_value)
            and self.grade.currentIndex() != 0
        ):
            self.score.setText(
                str(common_conversions.get_score_from_grade(self.grade.currentIndex()))
            )

    def delete_course(self):
        """Remove a specified course from the semester."""
        course_index = self.parent_semester.courses.index(self)
        self.parent_semester.courses.pop(course_index)
        self.deleteLater()

        for i in range(course_index, len(self.parent_semester.courses)):
            self.parent_semester.courses[i].title.setText(_("Course %d") % (i + 1))
