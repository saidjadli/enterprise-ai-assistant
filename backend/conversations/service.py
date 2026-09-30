import sqlite3
from datetime import datetime


DATABASE_PATH = "/app/data/users.db"



def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )



def create_conversation(
    user_id,
    title
):

    conn = get_connection()
    cursor = conn.cursor()


    conversation_id = str(__import__("uuid").uuid4())


    now = datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        INSERT INTO conversations
        (
            id,
            user_id,
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            conversation_id,
            user_id,
            title,
            now,
            now
        )
    )


    conn.commit()
    conn.close()


    return conversation_id



def add_message(
    conversation_id,
    role,
    content
):

    conn = get_connection()
    cursor = conn.cursor()


    now = datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        INSERT INTO messages
        (
            conversation_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content,
            now
        )
    )


    conn.commit()
    conn.close()



def get_user_conversations(
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            title,
            created_at,
            updated_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (
            user_id,
        )
    )


    rows = cursor.fetchall()

    conn.close()


    conversations = []


    for row in rows:

        conversations.append(
            {
                "id": row[0],
                "title": row[1],
                "created_at": row[2],
                "updated_at": row[3]
            }
        )


    return conversations



def get_conversation_messages(
    conversation_id
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            role,
            content,
            created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (
            conversation_id,
        )
    )


    rows = cursor.fetchall()

    conn.close()


    messages = []


    for row in rows:

        messages.append(
            {
                "role": row[0],
                "content": row[1],
                "created_at": row[2]
            }
        )


    return messages