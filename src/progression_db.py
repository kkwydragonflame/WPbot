import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "progression.db"

def initialize_database():
    """
    Initializes the database by creating the necessary tables if they don't exist.
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS progression_checks (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                school_year TEXT NOT NULL,
                asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responded_at TIMESTAMP,
                PRIMARY KEY (guild_id, user_id, school_year)
            )
          """
        )
        connection.commit()

def has_user_been_prompted(guild_id, user_id, school_year):
    """
    Check if the user has already been prompted for progression this school year.
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        result = connection.execute(
            """
            SELECT 1
            FROM progression_checks 
            WHERE guild_id = ? 
              AND user_id = ? 
              AND school_year = ?
            """,
            (guild_id,user_id, school_year)
        ).fetchone()

        return result is not None

def record_user_prompt(guild_id, user_id, school_year):
    """
    Record that the user has been prompted for progression this school year.
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO progression_checks 
                (guild_id, user_id, school_year)
            VALUES (?, ?, ?)
            """,
            (guild_id, user_id, school_year)
        )
        connection.commit()