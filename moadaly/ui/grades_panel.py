"""A Grades panel where you can create semesters, courses and insert the scores."""

from gettext import gettext as _
from typing import Optional
from uuid import uuid4

from PySide6 import QtCore, QtGui, QtWidgets

from moadaly import common_conversions


class GradesPanel(QtWidgets.QWidget):
    """A panel to display semesters, and to handle the addition of new semesters."""

    panel_calculation_changed = QtCore.Signal()
    semester_created = QtCore.Signal(str, str)
    semester_deleted = QtCore.Signal(str)
    course_created = QtCore.Signal(str, str)
    course_deleted = QtCore.Signal(str)
    course_name_updated = QtCore.Signal(str, str)
    course_score_updated = QtCore.Signal(str, float)
    course_credits_updated = QtCore.Signal(str, int)

    def __init__(self, parent_profile_id: str, point_scale: int) -> None:
        """Initialize base components of the panel."""
        super().__init__()

        self.parent_profile_id = parent_profile_id
        self.point_scale = point_scale

        self.semesters: list[SemesterWidget] = []

        self.total_points = 0.0
        self.total_credits = 0

        self.panel_layout = QtWidgets.QVBoxLayout(self)

        self.scroll_area = QtWidgets.QScrollArea()

        add_semester_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("list-add"),
            _("New Semester"),
        )
        add_semester_button.setStyleSheet("background-color: green; padding: 0 35px;")
        add_semester_button.setFixedHeight(35)
        add_semester_button.clicked.connect(self.add_new_semester)
        self.panel_layout.addStretch()
        self.panel_layout.addWidget(
            add_semester_button,
            alignment=QtCore.Qt.AlignCenter,
        )
        self.panel_layout.addStretch()

        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        # FIX: How scroll area behaive in small window size.
        self.scroll_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Maximum,
        )
        self.scroll_area.setWidget(self)

    def resize_scroll_area(self, window_size: tuple) -> None:
        """If main window got resized this function will be called with the new size."""
        # FIX: Maybe there is a better factor.
        self.scroll_area.setFixedHeight(int(window_size[1] * 2.3 / 3))

    def calculate_panel(self) -> None:
        """Calculate the sum of the semesters points and credit units."""
        self.total_points = 0.0
        self.total_credits = 0

        for semester in self.semesters:
            self.total_points += semester.total_points.value()
            self.total_credits += semester.total_credits.value()

        # Send a signal with the new points and credits to be displayed.
        self.panel_calculation_changed.emit()

    def add_new_semester(self, semester_id: Optional[str] = None) -> None:
        """Add new semester widget to the grades panel."""
        semester = SemesterWidget(self, semester_id)
        semester.semester_calculation_updated.connect(self.calculate_panel)
        self.semesters.append(semester)
        self.panel_layout.insertWidget(len(self.semesters) - 1, semester)

        if not semester_id:
            self.semester_created.emit(semester.semester_id, self.parent_profile_id)


class SemesterWidget(QtWidgets.QWidget):
    """A semester that contain a list of corses, to be added to the grades panel."""

    # TODO: Add the ability to move the semester to another profile.

    semester_calculation_updated = QtCore.Signal()

    def __init__(self, parent_panel: GradesPanel, semester_id: Optional[str]) -> None:
        """Initialize a new semester and it's base components."""
        super().__init__()

        self.parent_panel = parent_panel
        self.semester_id: str = semester_id or uuid4().hex
        self.courses: list[CourseWidget] = []

        # Those are used to display the info and also to store the value.
        self.total_points = QtWidgets.QDoubleSpinBox()
        self.total_points.setMaximum(10000)

        self.total_credits = QtWidgets.QSpinBox()
        self.total_credits.setMaximum(10000)

        self._semester_gpa = QtWidgets.QDoubleSpinBox()
        self._semester_gpa.setDecimals(3)
        self._semester_gpa.setMaximum(10000)

        self._semester_grade = QtWidgets.QLineEdit(_("Undefined"))

        self.semester_layout = QtWidgets.QVBoxLayout(self)

        # Create the semester title bar.
        title_layout = QtWidgets.QHBoxLayout()

        self.title = QtWidgets.QLabel(
            _("<h2>Semester %d</h2>") % (len(self.parent_panel.semesters) + 1),
        )
        self.title.setToolTip(self.semester_id)
        self.title.setFixedHeight(35)
        title_layout.addWidget(self.title)

        title_layout.addStretch()

        delete_semester_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("delete"),
            "",
        )
        delete_semester_button.setToolTip(_("Delete Semester"))
        delete_semester_button.setFixedSize(35, 35)
        delete_semester_button.clicked.connect(self.delete_semester)
        title_layout.addWidget(delete_semester_button)

        self.semester_layout.addLayout(title_layout)

        #  TODO: Create a header for the courses.
        headers_layout = QtWidgets.QHBoxLayout()
        self.semester_layout.addLayout(headers_layout)

        semester_footer_layout = QtWidgets.QHBoxLayout()
        self.semester_layout.addLayout(semester_footer_layout)

        # Create a button to add a now course.
        add_course_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("list-add"),
            "",
        )
        add_course_button.setStyleSheet("background-color: green;")
        add_course_button.setFixedSize(35, 35)
        add_course_button.clicked.connect(self.add_new_course)
        semester_footer_layout.addWidget(add_course_button)

        semester_footer_layout.addStretch(2)

        semester_footer_layout.addWidget(QtWidgets.QLabel(_("GPA")))
        self._semester_gpa.setReadOnly(True)
        self._semester_gpa.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self._semester_gpa.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        semester_footer_layout.addWidget(self._semester_gpa)

        semester_footer_layout.addStretch(1)

        semester_footer_layout.addWidget(QtWidgets.QLabel(_("Credit Units")))
        self.total_credits.setReadOnly(True)
        self.total_credits.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.total_credits.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        semester_footer_layout.addWidget(self.total_credits)

        semester_footer_layout.addStretch(1)

        semester_footer_layout.addWidget(QtWidgets.QLabel("Points"))
        self.total_points.setReadOnly(True)
        self.total_points.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.total_points.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        semester_footer_layout.addWidget(self.total_points)

        semester_footer_layout.addStretch(1)

        semester_footer_layout.addWidget(QtWidgets.QLabel(_("Grade")))
        self._semester_grade.setReadOnly(True)
        # TODO: Enable after being able to calculate the Grade.
        self._semester_grade.setDisabled(True)
        self._semester_grade.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        semester_footer_layout.addWidget(self._semester_grade)

        semester_footer_layout.addStretch(2)

    def calculate_semester(self) -> None:
        """Calculate the sum of points and the sum of credits in the semester."""
        total_points_value = 0.0
        total_credits_value = 0

        for course in self.courses:
            total_points_value += course.points.value()
            total_credits_value += course.credit.value()

        self.total_points.setValue(total_points_value)
        self.total_credits.setValue(total_credits_value)

        # TODO: calculate semester grade after implementing better point_scale config.
        # self._semester_grade.setText()  # noqa: ERA001

        if total_credits_value:
            self._semester_gpa.setValue(total_points_value / total_credits_value)

        # Send signal to recalculate panel.
        self.semester_calculation_updated.emit()

    def delete_semester(self) -> None:
        """Confirm then remove a specified semester from the grades panel."""
        semester_index = self.parent_panel.semesters.index(self)

        confirm_dialog = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Warning,
            _("Delete Semester | Moadaly"),
            _("Are you sure that you want to delete <b>Semester %d</b>?")
            % (semester_index + 1),
            buttons=QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )
        confirm_dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        confirm_dialog.setInformativeText(
            _(
                "That will permanently delete any courses under "
                "<b>Semester %d</b>, and any related data.",
            )
            % (semester_index + 1),
        )

        if confirm_dialog.exec() == QtWidgets.QMessageBox.Yes:
            self.parent_panel.semesters.pop(semester_index)
            self.deleteLater()

            for i in range(semester_index, len(self.parent_panel.semesters)):
                self.parent_panel.semesters[i].title.setText(
                    _("<h2>Semester %d</h2>") % (i + 1),
                )

            # Send signal to recalculate panel.
            # FIX: If it is the last semester in the panel, results not be updated.
            self.semester_calculation_updated.emit()
            self.parent_panel.semester_deleted.emit(self.semester_id)

    def add_new_course(
        self,
        course_id: Optional[str] = None,
        course_name: Optional[str] = None,
        course_score: Optional[float] = None,
        course_credit_units: Optional[int] = None,
    ) -> None:
        """Add new course widget to the semester."""
        course = CourseWidget(self, course_id)
        course.points_changed.connect(self.calculate_semester)
        self.courses.append(course)
        self.semester_layout.insertWidget(len(self.courses) + 1, course)

        if not course_id:
            self.parent_panel.course_created.emit(course.course_id, self.semester_id)

            # Move focus to the course name input when creating new course.
            course.name.setFocus()

        if course_name:
            course.name.setText(course_name)
        if course_score:
            course.score.setValue(course_score)
        if course_credit_units:
            course.credit.setValue(course_credit_units)


class CourseWidget(QtWidgets.QWidget):
    """A course that can be added inside a semester."""

    points_changed = QtCore.Signal()

    def __init__(
        self,
        parent_semester: SemesterWidget,
        course_id: Optional[str],
    ) -> None:
        """Initialize a new course and it's components."""
        super().__init__()

        self.course_id: str = course_id or uuid4().hex
        self.parent_semester = parent_semester

        self.course_layout = QtWidgets.QHBoxLayout(self)

        self.title = QtWidgets.QLabel(
            _("<h4>Course %d:</h4>") % (len(self.parent_semester.courses) + 1),
        )
        self.title.setToolTip(self.course_id)
        self.course_layout.addWidget(self.title)

        self.name = QtWidgets.QLineEdit()
        self.name.textChanged.connect(self.name_changed)
        self.course_layout.addWidget(self.name)

        self.score = QtWidgets.QDoubleSpinBox()
        # TODO: Change range accourding to the selected calculation system.
        self.score.setRange(0.0, 100.0)
        self.score.setSingleStep(0.25)
        self.score.valueChanged.connect(self.score_changed)
        self.score.valueChanged.connect(self.update_points)
        self.course_layout.addWidget(self.score)

        self.credit = QtWidgets.QSpinBox()
        self.credit.setMaximum(100000)
        self.credit.valueChanged.connect(self.update_points)
        self.credit.valueChanged.connect(self.credit_changed)
        self.course_layout.addWidget(self.credit)

        self.grade = QtWidgets.QComboBox()
        self.grade.addItems(common_conversions.grades)
        self.grade.currentIndexChanged.connect(self.grade_changed)
        self.course_layout.addWidget(self.grade)

        self.points = QtWidgets.QDoubleSpinBox()
        self.points.setReadOnly(True)
        self.points.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.points.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.points.setMaximum(10000)
        self.course_layout.addWidget(self.points)

        self.delete_course_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("delete"),
            "",
        )
        self.delete_course_button.setToolTip(_("Delete Course"))
        self.delete_course_button.setFixedSize(30, 30)
        self.delete_course_button.clicked.connect(self.delete_course)
        self.course_layout.addWidget(self.delete_course_button)

    def update_points(self) -> None:
        """Update the points when the score or the credit units are changed."""
        self.points.setValue(
            common_conversions.score_to_gpa(
                self.parent_semester.parent_panel.point_scale,
                self.score.value(),
            )
            * self.credit.value(),
        )

        # Send signal to recalculate semester.
        self.points_changed.emit()

    def score_changed(self) -> None:
        """Change the grade when the score is changed."""
        try:
            self.grade.setCurrentIndex(
                common_conversions.get_grade_from_score(self.score.value()),
            )
        except ValueError:
            # When we have empty string, set it to index zero (Undefined).
            self.grade.setCurrentIndex(0)

        # Push new score to the database.
        self.parent_semester.parent_panel.course_score_updated.emit(
            self.course_id,
            self.score.value(),
        )

    def credit_changed(self) -> None:
        """Push new credit units to the database."""
        self.parent_semester.parent_panel.course_credits_updated.emit(
            self.course_id,
            self.credit.value(),
        )

    def name_changed(self) -> None:
        """Push new name to the database."""
        self.parent_semester.parent_panel.course_name_updated.emit(
            self.course_id,
            self.name.text(),
        )

    def grade_changed(self) -> None:
        """Change the score when the grade is changed."""
        try:
            score_value: float = self.score.value()
        except ValueError:
            # When we have empty string.
            score_value = 0.0

        if (
            self.grade.currentIndex()
            != common_conversions.get_grade_from_score(score_value)
            and self.grade.currentIndex() != 0
        ):
            self.score.setValue(
                common_conversions.get_score_from_grade(self.grade.currentIndex()),
            )

    def delete_course(self) -> None:
        """Remove a specified course from the semester."""
        course_index = self.parent_semester.courses.index(self)
        self.parent_semester.courses.pop(course_index)
        self.deleteLater()

        for i in range(course_index, len(self.parent_semester.courses)):
            self.parent_semester.courses[i].title.setText(
                _("<h4>Course %d</h4>") % (i + 1),
            )

        # Send signal to recalculate semester.
        # FIX: If it is the last course in the semester, results not be updated.
        self.points_changed.emit()
        self.parent_semester.parent_panel.course_deleted.emit(self.course_id)
