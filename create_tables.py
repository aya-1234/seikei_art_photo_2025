import sqlite3

DB_NAME = 'database.db'

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # authors テーブル作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        instagram_url TEXT,
        twitter_url TEXT
    );
    """)

    # works テーブル作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS works (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER,
        image TEXT,
        title TEXT,
        caption TEXT,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    );
    """)

    # visits テーブル作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_id TEXT NOT NULL,
        author_id INTEGER,
        tap_time DATETIME,
        visit_time DATETIME,
        exit_time DATETIME,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("テーブルを作成しました！")