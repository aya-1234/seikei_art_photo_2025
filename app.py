from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import sqlite3
from datetime import datetime, timedelta
import logging
import uuid
import hashlib


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションを使用するための秘密鍵

# ログ設定
logging.basicConfig(filename='app.log', level=logging.ERROR)


author = {
    "fasfdasfawfa": "author"
}
hash = author

def get_author_visit_data():
    """
    作家ごとのタップ数と滞在時間を集計する
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.name, 
            COUNT(v.id) AS tap_count, 
            SUM(strftime('%s', v.exit_time) - strftime('%s', v.tap_time)) AS total_duration
        FROM authors a
        LEFT JOIN visits v ON a.id = v.author_id
        GROUP BY a.name
        ORDER BY tap_count DESC;
    """)
    author_data = cursor.fetchall()
    conn.close()
    return author_data
def get_detailed_visit_data():
    """
    詳細な訪問情報を取得する
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            a.name,  -- 作家名
            strftime('%H:%M:%S', v.tap_time) AS tap_time,  -- タップされた時間
            v.visit_time,  -- 訪問日時
            CASE WHEN v.exit_time IS NOT NULL THEN (strftime('%s', v.exit_time) - strftime('%s', v.tap_time)) ELSE 0 END AS duration  -- 滞在時間
        FROM visits v
        JOIN authors a ON v.author_id = a.id
        ORDER BY v.visit_time DESC
        LIMIT 100;  -- 取得するレコード数を制限 (パフォーマンス対策)
    """)
    visit_details = cursor.fetchall()
    conn.close()
    return visit_details

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # 辞書型でデータを取得
    return conn

# セッションからvisitor_idを取得、なければ新しく生成
def get_visitor_id():
    if 'visitor_id' not in session:
        session['visitor_id'] = str(uuid.uuid4())  # 新しいUUIDを生成
    return session['visitor_id']

# 作家情報を取得
def get_author_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
    author = cursor.fetchone()
    conn.close()
    return author

# 作品詳細を取得
def get_works_by_author(author_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, image FROM works WHERE author_id = ?", (author_id,))
    works = cursor.fetchall()
    conn.close()

    # works をディクショナリのリストに変換する
    works_list = []
    for work in works:
        works_list.append({
            'id': work[0],
            'title': work[1],
            'image': work[2]
        })
    return works_list

def get_work_by_index(author_id, work_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM works WHERE author_id = ? AND id = ?", (author_id, work_id))
    work = cursor.fetchone()
    conn.close()
    return work

# 訪問記録をデータベースに保存
def log_visit(visitor_id, author_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visits (visitor_id, author_id, tap_time, visit_time, exit_time)
            VALUES (?, ?, ?, ?, NULL)
        ''', (visitor_id, author_id, datetime.now(), datetime.now()))
        conn.commit()
    except Exception as e:
        logging.error(f"Error while logging visit: {e}")
    finally:
        conn.close()

def insert_visits():
    """
    visitsテーブルに訪問記録を挿入する関数
    visitor_idはセッションから取得し、author_idはauthor_nameから取得する
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Flaskセッションからvisitor_idを取得
        visitor_id = session.get('visitor_id')
        if not visitor_id:
            print("Error: visitor_id not found in session.")
            return  # visitor_idがない場合は関数を終了

        # author_nameからauthor_idを取得
        cursor.execute('SELECT id FROM authors WHERE name = ?', (author_name,))
        author_id_row = cursor.fetchone()

        if author_id_row:
            author_id = author_id_row[0]
        else:
            print(f"Error: author_id not found for author_name: {author_name}")
            return  # author_idがない場合は関数を終了

        # 訪問情報をvisitsテーブルに挿入
        cursor.execute('''
            INSERT INTO visits (visitor_id, author_id, tap_time, visit_time)
            VALUES (?, ?, ?, ?)
        ''', (visitor_id, author_id, tap_time, visit_time))

        conn.commit()
        print(f"Visit recorded for visitor_id: {visitor_id}, author_id: {author_id}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()  # エラー発生時はロールバック

    finally:
        conn.close()
        print("Database connection closed.")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_author_visit_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.name, 
            COUNT(v.id) AS tap_count, 
            SUM(CASE WHEN v.exit_time IS NOT NULL THEN strftime('%s', v.exit_time) - strftime('%s', v.tap_time) ELSE 0 END) AS total_duration
        FROM authors a
        LEFT JOIN visits v ON a.id = v.author_id
        GROUP BY a.name
        ORDER BY tap_count DESC;
    """)
    author_data = cursor.fetchall()
    conn.close()
    return author_data

def get_hourly_visit_counts(hours=24):
    """
    過去 `hours` 時間の時間ごとのアクセス数を取得する
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 現在時刻から指定された時間前の時刻を計算
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    cursor.execute("""
        SELECT
            strftime('%Y-%m-%d %H:00:00', tap_time) AS hour,
            COUNT(*)
        FROM visits
        WHERE tap_time BETWEEN ? AND ?
        GROUP BY hour
        ORDER BY hour
    """, (start_time, end_time))

    hourly_counts = cursor.fetchall()
    conn.close()

    # 結果を辞書形式に変換 (例: {'2023-10-27 10:00:00': 10, '2023-10-27 11:00:00': 5, ...})
    return {row['hour']: row[1] for row in hourly_counts}

def get_weekly_visit_counts(weeks=4):
    """
    過去 `weeks` 週間分の週ごとの訪問者数を取得する。

    Args:
        weeks (int): 集計する週数。

    Returns:
        dict: 週の開始日をキー、訪問者数を値とする辞書。
              例: {'2023-10-23': 15, '2023-10-30': 22, ...}
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 現在の日付から指定された週数前の日付を計算
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=weeks * 7)

    # 週の開始日 (月曜日) と訪問者数を取得するクエリ
    cursor.execute("""
        SELECT
            strftime('%Y-%m-%d', date(visit_time, 'weekday 0', '-6 days')) AS week_start,
            COUNT(DISTINCT visitor_id)  -- 重複を除いた訪問者数をカウント
        FROM visits
        WHERE visit_time BETWEEN ? AND ?
        GROUP BY week_start
        ORDER BY week_start
    """, (start_date, end_date))

    weekly_counts = cursor.fetchall()
    conn.close()

    # 結果を辞書形式に変換
    return {row['week_start']: row[1] for row in weekly_counts}



#admin用ページ
@app.route("/aDm1n")
def admin():
    author_visit_data = get_author_visit_data()

    # グラフ用のデータを作成
    labels_author = [data[0] for data in author_visit_data]
    tap_counts = [data[1] for data in author_visit_data]
    durations = [data[2] for data in author_visit_data]

    # 時間別アクセス数
    hourly_counts = get_hourly_visit_counts()
    labels_hourly = list(hourly_counts.keys())
    data_hourly = list(hourly_counts.values())

        # 週ごとの訪問者数を取得
    weekly_counts = get_weekly_visit_counts()
    labels_weekly = list(weekly_counts.keys())
    data_weekly = list(weekly_counts.values())

    return render_template(
        "admin.html",
        labels_author=labels_author,
        tap_counts=tap_counts,
        durations=durations,
        labels_hourly=labels_hourly,
        data_hourly=data_hourly,
        labels_weekly=labels_weekly,
        data_weekly=data_weekly
    )

@app.route("/log_exit/<author_name>/<int:work_id>", methods=['POST'])
def log_exit(author_name, work_id):
    visitor_id = get_visitor_id()
    author = get_author_by_name(author_name)

    if not author:
        return "Author not found", 404

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE visits
            SET exit_time = ?
            WHERE visitor_id = ? AND author_id = ? AND exit_time IS NULL
        ''', (datetime.now(), visitor_id, author["id"]))
        conn.commit()
    except Exception as e:
        logging.error(f"Error while logging exit: {e}")
    finally:
        conn.close()

    return redirect(url_for('author', author_name=author_name))

# ルート: 作家一覧ページ
@app.route("/")
def start():
    return render_template("start.html")

@app.route("/top-art")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM authors")
    authors = [row["name"] for row in cursor.fetchall()]
    conn.close()
    return render_template("index.html", authors=authors)

# 作家詳細ページ (ハッシュ値を元に作家情報を取得)
@app.route("/top-art/author/<author_name>")
def author(author_name):  # パラメータ名を author_name に修正
    conn = get_db_connection()
    cursor = conn.cursor()

    # 作家データを取得 (データベースでフィルタリング)
    author_data = get_author_by_name(author_name)
    if not author_data:
        conn.close()  # get_author_by_name の中で close しているが、念のため
        return f"作家 '{author_name}' は見つかりませんでした。", 404

    works = get_works_by_author(author_data["id"])  # 作品データ取得
    conn.close() #明示的にclose
    return render_template("author.html", author=author_data, works=works)

# 作家名と作品IDを使って作品詳細ページを表示する
@app.route("/top-art/work/<author_name>/<int:work_id>")
def work_by_name_and_id(author_name, work_id):
    visitor_id = get_visitor_id()

    # 作家情報を取得
    author = get_author_by_name(author_name)
    if not author:
        return "作家が見つかりませんでした", 404

    # 作品情報を取得
    work = get_work_by_index(author["id"], work_id)
    if not work:
        return "作品が見つかりませんでした", 404

    # 訪問記録を挿入
    log_visit(visitor_id, author["id"])

    # work.html に必要な情報を渡す
    return render_template("work.html", author=author, work=work)

@app.route('/top-art/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')


if __name__ == "__main__":
    app.run(debug=True)
