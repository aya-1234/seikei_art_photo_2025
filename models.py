import sqlite3

DB_NAME = "database.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # authors テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        instagram_url TEXT,
        twitter_url TEXT
    )
    """)

    # works テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS works (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER,
        image TEXT NOT NULL,
        title TEXT NOT NULL,
        caption TEXT,
        FOREIGN KEY (author_id) REFERENCES authors (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
