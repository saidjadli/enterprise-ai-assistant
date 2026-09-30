import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/users.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
        """
    )

    connection.commit()

    connection.close()


def get_user_by_email(email: str):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    return user


def create_user(
    username: str,
    email: str,
    password_hash: str,
    role: str = "user"
):

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO users (
            username,
            email,
            password_hash,
            role
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            email,
            password_hash,
            role
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id