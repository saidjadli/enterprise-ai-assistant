import sqlite3
import uuid
from datetime import datetime


DATABASE = "/app/data/users.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_conversation(user_id: int, title: str):
    conn = get_connection()
    cursor = conn.cursor()

    conversation_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO conversations
        (
            id,
            user_id,
            title
        )
        VALUES (?, ?, ?)
        """,
        (
            conversation_id,
            user_id,
            title
        )
    )

    conn.commit()
    conn.close()

    return conversation_id



def add_message(
    conversation_id: str,
    role: str,
    content: str
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (
            conversation_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content
        )
    )

    conn.commit()
    conn.close()



def get_conversation_messages(conversation_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
        """,
        (conversation_id,)
    )

    messages = cursor.fetchall()

    conn.close()

    return [
        {
            "role": message[0],
            "content": message[1]
        }
        for message in messages
    ]