"""Testing the database."""

import json
import random
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import pytest

from moadaly import database

temp_dir = TemporaryDirectory()
environ["HOME"] = temp_dir.name


# Data for testing.
profile2 = database.ProfileData(uuid4().hex, "Test Profile", "#000000", 5)
semester1_id = uuid4().hex
semester2_id = uuid4().hex
course1 = database.CourseData(
    uuid4().hex,
    "Math-111",
    random.uniform(0.0, 100.0),
    random.randint(0, 999),
)
course2 = database.CourseData(
    uuid4().hex,
    "Math-112",
    random.uniform(0.0, 100.0),
    random.randint(0, 999),
)


def test_createing_database() -> None:
    """Test Creating new database with every possible way."""
    assert database.Database(Path(str(temp_dir.name)).joinpath("database.sqlite3"))

    environ["XDG_DATA_HOME"] = temp_dir.name
    assert database.Database()

    environ["XDG_DATA_HOME"] = ""
    assert database.Database()


@pytest.mark.dependency
def test_profile() -> None:
    """Test creating new profile in the database, read it, select and delete it."""
    db = database.Database()

    # Auto creating new profile when database is empty.
    profile1 = db.get_current_profile_data()
    assert isinstance(profile1, database.ProfileData)

    # Create new profile.
    db.create_new_profile(profile2.id, profile2.name, profile2.color)

    assert db.get_current_profile_data() == profile2

    # Change selected profile.
    db.update_profile_selected_time(profile1.id)

    assert db.get_current_profile_data() == profile1

    # Varify profiles data.
    assert db.get_profiles_data() == (profile1, profile2)

    # Delete profile.
    db.delete_profile(profile1.id)
    assert db.get_profiles_data() == (profile2,)


@pytest.mark.dependency(depends=["test_profile"])
def test_semester() -> None:
    """Test creating new semester in the database and deleting it."""
    db = database.Database()

    # Create new semesters.
    db.create_new_semester(semester1_id, profile2.id)
    db.create_new_semester(semester2_id, profile2.id)

    # Delete semester.
    db.delete_semester(semester1_id)


@pytest.mark.dependency(depends=["test_semester"])
def test_course() -> None:
    """Test creating new course in the database, read it, update and delete it."""
    db = database.Database()

    # Create new courses.
    db.create_new_course(course1.id, semester2_id)
    db.create_new_course(course2.id, semester2_id)

    # Update course data.
    db.update_course_name(course1.id, course1.name)
    db.update_course_name(course2.id, course2.name)
    db.update_course_score(course1.id, course1.score)
    db.update_course_score(course2.id, course2.score)
    db.update_course_credit_units(course1.id, course1.credit_units)
    db.update_course_credit_units(course2.id, course2.credit_units)

    # Varify courses data.
    assert db.get_courses_data(profile2.id) == {semester2_id: (course1, course2)}

    # Delete course.
    db.delete_course(course1.id)
    assert db.get_courses_data(profile2.id)[semester2_id] == (course2,)


@pytest.mark.dependency(depends=["test_course"])
def test_export_json() -> None:
    """Test the export to json file feature."""
    db = database.Database()

    file_path = Path.home().joinpath("exported_data.json")

    db.export_to_json(file_path)

    assert json.load(Path.open(file_path, "r")) == [
        {
            "profile_data": {
                "id": profile2.id,
                "name": profile2.name,
                "color": profile2.color,
                "point_scale": profile2.point_scale,
            },
            "semesters": [
                {
                    "semester_data": None,
                    "courses": [
                        {
                            "id": course2.id,
                            "name": course2.name,
                            "score": course2.score,
                            "credit_units": course2.credit_units,
                        },
                    ],
                },
            ],
        },
    ]


# def test_import_json() -> None:
#     """Test the import from json file feature."""  # noqa: ERA001
#     # Not yet implemented.
#     ...


@pytest.mark.dependency(depends=["test_profile"])
def test_profile_settings() -> None:
    """Test updating profile settings or the calculation system."""
    db = database.Database()

    db.change_point_scale(profile2.id, 4)
    assert db.get_current_profile_data().point_scale == 4


@pytest.mark.dependency(depends=["test_course"])
def test_database_relationship() -> None:
    """Deleting profiles or semesters is related to semesters or courses under them."""
    db = database.Database()

    db.delete_profile(profile2.id)
    assert db.get_profiles_data() == ()
    assert db.get_courses_data(profile2.id) == {}
