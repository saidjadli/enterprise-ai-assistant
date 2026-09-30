import sqlite3


DATABASE = "/app/data/users.db"


def migrate():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (

        id TEXT PRIMARY KEY,

        user_id INTEGER NOT NULL,

        title TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id TEXT NOT NULL,

        role TEXT NOT NULL,

        content TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
    )
    """)


    conn.commit()
    conn.close()


    print("Migration completed")


if __name__ == "__main__":
    migrate()