import hashlib, sqlite3, urllib.parse
from flask import Flask, render_template, url_for, abort, redirect
from typing import List, Tuple, Dict, Optional

app = Flask(__name__)
DB_NAME = "database.db"

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_author_by_name(author_name: str) -> Optional[sqlite3.Row]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE name = ?", (author_name,))
    author = cursor.fetchone()
    conn.close()
    return author

def get_works_by_author(author_id: int) -> List[Tuple[str, str]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, image FROM works WHERE author_id = ?", (author_id,))
    works = cursor.fetchall()
    conn.close()
    # 画像ファイル名をURLエンコード
    works = [(work[0], urllib.parse.quote(work[1])) for work in works]
    return works

def get_data() -> Dict[str, Dict[str, any]]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # これがないと、辞書形式でアクセスできない
    cursor = conn.cursor()

    # authors と works を JOIN して取得
    cursor.execute("""
    SELECT authors.name, authors.instagram_url, authors.twitter_url, works.image, works.title, works.caption
    FROM authors
    JOIN works ON authors.id = works.author_id
    """)

    data = cursor.fetchall()
    conn.close()

    # データを整理して返す（辞書形式）
    authors_data = {}
    for row in data:
        author_name = row["name"]  # rowが辞書のようにアクセスできるようになりました
        if author_name not in authors_data:
            authors_data[author_name] = {
                "instagram_url": row["instagram_url"],
                "twitter_url": row["twitter_url"],
                "works": []
            }
        authors_data[author_name]["works"].append({
            "image": row["image"],
            "title": row["title"],
            "caption": row["caption"]
        })

    return authors_data
@app.route("/")
def index():
    authors_data = get_data()
    author_names = list(authors_data.keys())  # 作者名のリストを作成
    return render_template("index.html", authors=author_names)

@app.route("/how_to_use")
def how_to_use():
    return render_template("how_to_use.html")

@app.route("/author/<author_name>")
def author(author_name):
    # 作家情報をデータベースから取得
    author = get_author_by_name(author_name)
    if author:
        author_id = author[0]  # IDは最初のカラムと仮定
        works = get_works_by_author(author_id)
        # authorオブジェクトもテンプレートに渡す
        return render_template("author.html", author=author, author_name=author_name, works=works)
    else:
        return f"作家 '{author_name}' は見つかりませんでした。", 404

@app.route("/work/<author_name>/<int:work_index>")
def work(author_name, work_index):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 作者のIDを取得
    cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
    author_id = cursor.fetchone()

    if author_id:
        author_id = author_id[0]

        # 作品情報を取得
        cursor.execute("""
        SELECT image, title, caption FROM works WHERE author_id = ? LIMIT 1 OFFSET ?
        """, (author_id, work_index))
        work_info = cursor.fetchone()

        if work_info:
            image, title, caption = work_info
            conn.close()
            return render_template("work.html", author_name=author_name, work={"image": image, "title": title, "caption": caption})
    conn.close()
    abort(404)


# 作品ページへのリダイレクトを追加
@app.route("/work_redirect/<author_name>/<int:work_index>")  # 旧URLからのリダイレクト用
def redirect_work(author_name, work_index):
    # work_index をハッシュ化
    work_id = hashlib.md5(str(work_index).encode()).hexdigest()[:4]  # 短縮化
    return redirect(url_for('work', author_name=author_name, work_index=work_index))

if __name__ == "__main__":
    app.run(debug=True)
