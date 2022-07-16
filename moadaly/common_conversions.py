"""Some common conversions."""


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


def score_to_5points_scale(score: float) -> float:
    """Convert the score the 5 points scale value."""
    if 100 >= score >= 95:
        return 5.0
    elif score >= 90:
        return 4.75
    elif score >= 85:
        return 4.5
    elif score >= 80:
        return 4.0
    elif score >= 75:
        return 3.5
    elif score >= 70:
        return 3.0
    elif score >= 65:
        return 2.5
    elif score >= 60:
        return 2.0
    else:
        return 1.0
