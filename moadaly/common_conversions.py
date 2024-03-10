"""Some common conversions."""

from gettext import gettext as _

grades = (
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
)

grades_colors = (
    "#FFFFFF",
    "#00FF00",
    "#47FF00",
    "#8DFF00",
    "#D4FF00",
    "#FFE400",
    "#FF9E00",
    "#FF5700",
    "#FF2300",
    "#FF0000",
)


class NotSupportedPointScaleError(ValueError):
    """Error to be raised when uncompatable point scale is passes to function."""

    def __init__(self, point_scale: int) -> None:
        """Error initalization function."""
        super().__init__(f"`{point_scale}` doesn't represent a supported point scale.")


def get_grade_from_gpa(point_scale: int, gpa: float) -> str:  # noqa: C901
    """Convert the gpa to a grade."""
    if point_scale == 5:
        if gpa >= 4.75:
            return grades[1]
        if gpa >= 4.5:
            return grades[2]
        if gpa >= 4.0:
            return grades[3]
        if gpa >= 3.5:
            return grades[4]
        if gpa >= 3.0:
            return grades[5]
        if gpa >= 2.5:
            return grades[6]
        if gpa >= 2.0:
            return grades[7]
        if gpa >= 1.0:
            return grades[8]

        return grades[9]

    if point_scale == 4:
        if gpa >= 4:
            return grades[1]
        if gpa >= 3.75:
            return grades[2]
        if gpa >= 3.5:
            return grades[3]
        if gpa >= 3.0:
            return grades[4]
        if gpa >= 2.5:
            return grades[5]
        if gpa >= 2.0:
            return grades[6]
        if gpa >= 1.5:
            return grades[7]
        if gpa >= 1.0:
            return grades[8]

        return grades[9]

    raise NotSupportedPointScaleError(point_scale)


def get_grade_from_score(score: float) -> int:
    """Convert the score to a number that refers to the grade."""
    if 100 >= score >= 95:
        return 1
    if score >= 90:
        return 2
    if score >= 85:
        return 3
    if score >= 80:
        return 4
    if score >= 75:
        return 5
    if score >= 70:
        return 6
    if score >= 65:
        return 7
    if score >= 60:
        return 8

    return 9


def get_score_from_grade(grade: int) -> int:
    """Convert the number that refers to the grade to a score."""
    if grade == 1:
        return 95
    if grade == 2:
        return 90
    if grade == 3:
        return 85
    if grade == 4:
        return 80
    if grade == 5:
        return 75
    if grade == 6:
        return 70
    if grade == 7:
        return 65
    if grade == 8:
        return 60

    return 0


def score_to_gpa(point_scale: int, score: float) -> float:  # noqa: C901
    """Convert the score to GPA based on the points scale value."""
    if point_scale == 5:
        if 100 >= score >= 95:
            return 5.0
        if score >= 90:
            return 4.75
        if score >= 85:
            return 4.5
        if score >= 80:
            return 4.0
        if score >= 75:
            return 3.5
        if score >= 70:
            return 3.0
        if score >= 65:
            return 2.5
        if score >= 60:
            return 2.0

        return 1.0

    if point_scale == 4:
        if 100 >= score >= 95:
            return 4.0
        if score >= 90:
            return 3.75
        if score >= 85:
            return 3.5
        if score >= 80:
            return 3.0
        if score >= 75:
            return 2.5
        if score >= 70:
            return 2.0
        if score >= 65:
            return 1.5
        if score >= 60:
            return 1.0

        return 0

    raise NotSupportedPointScaleError(point_scale)
