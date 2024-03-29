"""Deal with the database."""

import json
import sqlite3
from dataclasses import asdict, dataclass
from os import environ
from pathlib import Path
from time import time
from typing import Optional
from uuid import uuid4

from . import __about__


@dataclass
class ProfileData:
    """Data class for profile data."""

    id: str
    name: str
    color: str
    point_scale: int


@dataclass
class SemesterData:
    """Data class for semester data."""

    id: str


@dataclass
class CourseData:
    """Data class for course data."""

    id: str
    name: str
    score: float
    credit_units: int


class Database:
    """Manage the database."""

    def __init__(self, database_file: Optional[Path] = None) -> None:
        """Initialize some important variables."""
        if database_file:
            self.database_file = database_file
        else:
            # Use the XDG base directory.
            xdg_data_home = Path(
                environ.get("XDG_DATA_HOME", ""),
            ) or Path.home().joinpath(".local/share/")

            self.database_file = xdg_data_home.joinpath(
                __about__.APP_NAME,
                "database.sqlite3",
            )

        if not self.database_file.parent.exists():
            Path.mkdir(self.database_file.parent, parents=True)

        if not self.database_file.exists():
            self.create_database()

    def create_database(self) -> None:
        """Create the database and it's tables."""
        con = sqlite3.connect(self.database_file)
        cur = con.cursor()
        # The last_selected_time let us know which profile was selected most recent.
        cur.execute(
            """CREATE TABLE IF NOT EXISTS profiles
                    (id TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        color TEXT NOT NULL,
                        point_scale INTEGER,
                        last_selected_time INTEGER NOT NULL);""",
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS semesters
                    (id TEXT UNIQUE NOT NULL,
                        parent_profile_id TEXT NOT NULL,
                        FOREIGN KEY (parent_profile_id)
                        REFERENCES profiles (id)
                            ON DELETE CASCADE);""",
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS courses
                    (id TEXT UNIQUE NOT NULL,
                        parent_semester_id TEXT NOT NULL,
                        name TEXT,
                        score REAL,
                        credit_units INTEGER,
                        FOREIGN KEY (parent_semester_id)
                        REFERENCES semesters (id)
                            ON DELETE CASCADE);""",
        )
        con.close()

    def get_connection(self) -> sqlite3.Connection:
        """Check if there was a connection, then create new one if there wasn't."""
        if not hasattr(self, "connection"):
            if Path.exists(self.database_file):
                self.connection = sqlite3.connect(self.database_file)
                # Enable the foreign keys.
                self.connection.cursor().execute("PRAGMA foreign_keys = ON;")
            else:
                err_msg = "The database file was deleted while the app is running."
                raise RuntimeError(err_msg)
                # TODO: Display the error message in the GUI.

        return self.connection

    def close(self) -> None:
        """Close the current database connection."""
        if hasattr(self, "connection"):
            self.connection.commit()
            self.connection.close()
            del self.connection

    def create_new_profile(
        self,
        profile_id: str,
        profile_name: str,
        profile_color: str,
    ) -> None:
        """Add new profile to the profiles table."""
        # The rest of the parameters are NULL, the default settings will be used.
        self.get_connection().cursor().execute(
            """INSERT INTO profiles
                (id, name, color, point_scale, last_selected_time)
                    VALUES (?, ?, ?, 5, ?);""",
            (profile_id, profile_name, profile_color, time()),
        )
        self.close()

    def delete_profile(self, profile_id: str) -> None:
        """Delete a profile with all it's semesters and courses."""
        self.get_connection().cursor().execute(
            "DELETE FROM profiles WHERE id = ?;",
            (profile_id,),
        )
        self.close()

    def get_current_profile_data(self) -> ProfileData:
        """Return the current selected profile."""
        try:
            data = ProfileData(
                *(
                    self.get_connection()
                    .cursor()
                    .execute(
                        """SELECT
                            id, name, color, point_scale
                                FROM profiles ORDER BY last_selected_time DESC;""",
                    )
                    .fetchone()
                ),
            )
        except TypeError:
            # When there is no profile in the database.
            # TODO: Use Moadaly's logo color as default.
            data = ProfileData(uuid4().hex, "default", "#000000", 5)
            self.create_new_profile(data.id, data.name, data.color)

        return data

    def update_profile_selected_time(self, selected_profile_id: str) -> None:
        """Update last_selected_time when selecting another profile."""
        self.get_connection().cursor().execute(
            "UPDATE profiles SET last_selected_time = ? WHERE id = ?",
            (time(), selected_profile_id),
        )
        self.close()

    def get_profiles_data(self) -> tuple[ProfileData, ...]:
        """Return a list with the profiles data from the database."""
        self.get_connection().row_factory = lambda _cursor, row: ProfileData(*row)
        return tuple(
            self.get_connection()
            .cursor()
            .execute(
                """SELECT id, name, color, point_scale
                        FROM profiles ORDER BY last_selected_time DESC;""",
            )
            .fetchall(),
        )

    def create_new_semester(self, semester_id: str, parent_profile_id: str) -> None:
        """Add new semester in the semesters table."""
        self.get_connection().cursor().execute(
            """INSERT INTO semesters (id, parent_profile_id) VALUES (?, ?);""",
            (semester_id, parent_profile_id),
        )
        self.close()

    def delete_semester(self, semester_id: str) -> None:
        """Delete a semester and it's courses from the semesters table."""
        self.get_connection().cursor().execute(
            """DELETE FROM semesters WHERE id = ?;""",
            (semester_id,),
        )
        self.close()

    def create_new_course(self, course_id: str, parent_semester_id: str) -> None:
        """Add new course in the courses table."""
        self.get_connection().cursor().execute(
            """INSERT INTO courses (id, parent_semester_id) VALUES (?, ?);""",
            (course_id, parent_semester_id),
        )
        self.close()

    def delete_course(self, course_id: str) -> None:
        """Delete a course from the courses table."""
        self.get_connection().cursor().execute(
            """DELETE FROM courses WHERE id = ?;""",
            (course_id,),
        )
        self.close()

    def get_courses_data(self, profile_id: str) -> dict[str, tuple[CourseData, ...]]:
        """Get courses data from a profile id."""
        self.get_connection().row_factory = lambda _cursor, row: SemesterData(*row)
        semesters = tuple(
            self.get_connection()
            .cursor()
            .execute(
                """SELECT id FROM semesters WHERE parent_profile_id = ?;""",
                (profile_id,),
            )
            .fetchall(),
        )

        # TODO: Figure a way to do the same thing with only one query.

        self.get_connection().row_factory = lambda _cursor, row: CourseData(*row)
        return {
            semester.id: tuple(
                self.get_connection()
                .cursor()
                .execute(
                    """SELECT id, name, score, credit_units
                            FROM courses WHERE parent_semester_id = ?;""",
                    (semester.id,),
                )
                .fetchall(),
            )
            for semester in semesters
        }

    def update_course_name(self, course_id: str, course_name: str) -> None:
        """Update course name."""
        self.get_connection().cursor().execute(
            "UPDATE courses SET name = ? WHERE id = ?",
            (course_name, course_id),
        )
        self.close()

    def update_course_score(self, course_id: str, course_score: float) -> None:
        """Update course score."""
        self.get_connection().cursor().execute(
            "UPDATE courses SET score = ? WHERE id = ?",
            (course_score, course_id),
        )
        self.close()

    def update_course_credit_units(
        self,
        course_id: str,
        course_credit_units: int,
    ) -> None:
        """Update course credit units."""
        self.get_connection().cursor().execute(
            "UPDATE courses SET credit_units = ? WHERE id = ?",
            (course_credit_units, course_id),
        )
        self.close()

    def export_to_json(self, file_path: Path) -> None:
        """Convert the database to json format and save it to a file."""
        data = [
            {
                "profile_data": asdict(profile),
                "semesters": tuple(
                    {
                        # This key is for further functionalities of the app.
                        "semester_data": None,
                        "courses": tuple(
                            asdict(course_data) for course_data in courses_data
                        ),
                    }
                    for semester_id, courses_data in self.get_courses_data(
                        profile.id,
                    ).items()
                ),
            }
            for profile in self.get_profiles_data()
        ]

        self.close()

        json.dump(data, Path.open(file_path, "w"), ensure_ascii=False, indent=2)

    def import_from_json(self, file_path: Path) -> None:
        """Import json file data to the database."""
        # TODO: Implement import from json file to database.

    def change_point_scale(self, profile_id: str, new_point_scale: int) -> None:
        """Update the point scale in a profile."""
        self.get_connection().cursor().execute(
            """UPDATE profiles SET point_scale = ? WHERE id = ?""",
            (new_point_scale, profile_id),
        )
