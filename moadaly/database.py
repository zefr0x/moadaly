"""Deal with the database."""
from typing import Optional
import sqlite3
from time import time
from uuid import uuid4
from dataclasses import dataclass


@dataclass
class ProfileData:
    """Data class for profile data."""

    id: str  # Yes, i know...
    name: str
    color: str
    point_scale: Optional[int]
    grading_system: Optional[int]
    score_scale: Optional[int]


class Database:
    """Manage the database."""

    def __init__(self):
        """Initialize some important variables."""
        # TODO Use the XDG standard directory "~/.local/share".
        self.database_file = "./db.sqlite3"

    def get_connection(self) -> sqlite3.Connection:
        """Check if there was a connection or not, then create new one if there wasn't."""
        if not hasattr(self, "connection"):
            self.connection = sqlite3.connect(self.database_file)

            # Create the database tables if the were not there.
            # The last_selected_time let us know which profile was selected most recent.
            self.connection.cursor().execute(
                """CREATE TABLE IF NOT EXISTS profiles
                        (id TEXT UNIQUE NOT NULL,
                         name TEXT NOT NULL,
                         color TEXT NOT NULL,
                         point_scale INTEGER,
                         grading_system INTEGER,
                         score_scale INTEGER,
                         last_selected_time INTEGER NOT NULL);"""
            )
        return self.connection

    def close(self) -> None:
        """Close the current database connection."""
        if hasattr(self, "connection"):
            self.connection.commit()
            self.connection.close()
            del self.connection

    def create_new_profile(self, profile_id, profile_name, profile_color) -> None:
        """Add new profile to the profiles table."""
        # The rest of the parameters are NULL, which means that the default settings will be used.
        self.get_connection().cursor().execute(
            "INSERT INTO profiles (id, name, color, last_selected_time) VALUES (?, ?, ?, ?);",
            (profile_id, profile_name, profile_color, time()),
        )
        self.close()

    def delete_profile(self, profile_id) -> None:
        """Delete a profile with all it's semesters and courses."""
        self.get_connection().cursor().execute(
            "DELETE FROM profiles WHERE id = ?;",
            (profile_id,),
        )
        self.close()
        # TODO Delete all semesters and courses related to the profile.

    def get_current_profile_data(self) -> ProfileData:
        """Return the current selected profile."""
        try:
            data = ProfileData(
                *(
                    self.get_connection()
                    .cursor()
                    .execute(
                        """SELECT id, name, color, point_scale, grading_system, score_scale
                                FROM profiles ORDER BY last_selected_time DESC;"""
                    )
                    .fetchone()
                )
            )
            self.close()
        except TypeError:
            # When there is no profile in the database.
            # TODO Use Moadaly's logo color as default.
            data = ProfileData(uuid4().hex, "default", "#000000", None, None, None)
            self.create_new_profile(data.id, data.name, data.color)

        return data

    def update_profile_selected_time(self, selected_profile_id) -> None:
        """Update last_selected_time when selecting another profile."""
        self.get_connection().cursor().execute(
            "UPDATE profiles SET last_selected_time = ? WHERE id = ?",
            (time(), selected_profile_id),
        )
        self.close()

    def get_profiles_list(self) -> list[ProfileData]:
        """Return a list with the profiles data from the database."""
        self.get_connection().row_factory = lambda cursor, row: ProfileData(*row)
        profiles = (
            self.get_connection()
            .cursor()
            .execute(
                """SELECT id, name, color, point_scale, grading_system, score_scale
                        FROM profiles ORDER BY last_selected_time DESC;"""
            )
            .fetchall()
        )
        self.close()

        return profiles
