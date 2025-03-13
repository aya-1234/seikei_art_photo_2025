import hashlib 
from flask import Flask, render_template, url_for, abort, redirect

app = Flask(__name__)

# 作品情報を辞書で管理。作者ごとに作品をリストで持つ
authors = {
    "内田絢汰": {
        "works": [
            {"image": "images/aaa.jpeg" , "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "instagram_url": "https://www.instagram.com/aya___cmr?igsh=MWl1YXY2eW50ejc0bQ%3D%3D&utm_source=qr",
        "twitter_url": "https://x.com/Aya7__Gaming",
    },
    "波多野ひなた": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "instagram_url": "https://www.instagram.com/ultra_happychan?igsh=bmhtZnN0M2hjNGVo&utm_source=qr",
        "twitter_url": "https://x.com/ultra_happychan?s=21&t=toYGO5301kXqijZqUquxQw",
    },
    "戸高花音": {
        "works": [
            {"image": "images/裏側まで.jpeg", "title": "裏側まで", "caption": "デジタル"},
            {"image": "images/キャプションなし1.jpeg", "title": "", "caption": "Canon EOS kiss X9"},
            {"image": "images/キャプションなし2.jpeg", "title": "", "caption": "Canon EOS kiss X9"},
            {"image": "images/キャプションなし3.jpeg", "title": "", "caption": "Canon EOS kiss X9"},
        ],
        "instagram_url": "https://www.instagram.com/oozzz_u_u?igsh=NGc2ejRtMDAzaTV5&utm_source=qr",
    },
    "永井杏奈": {
        "works": [
            {"image": "images/2人の秘密　真実を隠す子1.jpg", "title": "2人の秘密　真実を隠す子", "caption": "アクリルガッシュ"},
            {"image": "images/2人の秘密　真実を隠す子2.jpg", "title": "2人の秘密　真実を隠す子", "caption": "アクリルガッシュ"},
        ],
        "instagram_url": "https://www.instagram.com/nemunieru_724?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
    },
    "矢野陽菜": {
        "works": [
            {"image": "images/末枯れる.jpg", "title": "末枯れる", "caption": ""},
        ],
    },
    "細谷有未": {
        "works": [
            {"image": "images/華がある、バレリーナ.jpeg", "title": "華がある、バレリーナ1", "caption": "写真 スケッチブック ボールペン"},
            {"image": "images/華がある、バレリーナ.jpeg", "title": "華がある、バレリーナ2", "caption": "写真 スケッチブック ボールペン"},
            {"image": "images/華がある、バレリーナ.jpeg", "title": "華がある、バレリーナ3", "caption": "写真 スケッチブック ボールペン"},
            {"image": "images/街通り.jpeg", "title": "街通り", "caption": "canonEOS80D"},
            {"image": "images/街通り2.jpeg", "title": "街通り", "caption": "canonEOS80D"},
            {"image": "images/街通り3.jpeg", "title": "街通り", "caption": "canonEOS80D"},
            {"image": "images/街通り4.jpeg", "title": "街通り", "caption": "canonEOS80D"},
        ],
        "instagram_url": "https://www.instagram.com/purasu_photo22?igsh=MWZ6dmF3b2NyNzJlMQ%3D%3D&utm_source=qr",
    },
    "石川葵": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "三宅梨菜": {
        "works": [
            {"image": "images/飛翔の瞬間.jpg", "title": "飛翔の瞬間", "caption": "CLIP STUDIO PAINT"},
            {"image": "images/創造の空間.jpg", "title": "創造の空間", "caption": "CLIP STUDIO PAINT"},
            {"image": "images/陸の果てまで歩いた.jpg", "title": "陸の果てまで歩いた", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/睡蓮.jpg", "title": "睡蓮", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/花明り.jpg", "title": "花明り", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/セレナーデ.png", "title": "セレナーデ", "caption": "CLIP STUDIO PAINT"},
        ],
    },
    "川島虹": {
        "works": [
            {"image": "images/贈り物.jpg", "title": "贈り物", "caption": "水彩、色鉛筆、マルチライナー"},
        ],
    },
    "北村明日香": {
        "works": [
            {"image": "images/空風も和らぐ日.jpg", "title": "空風も和らぐ日", "caption": "OLYMPUS E-M10 MarkⅢ"},
        ],
    },
    "奥村天": {
        "works": [
            {"image": "images/ある古代の一日.jpg", "title": "ある古代の一日", "caption": "アクリリックカラー、筆、キャンバス"},
        ],
    },
    "高村咲弥花": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "鍛治美羽": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "西岡愛結": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "梶田恵": {
        "works": [
            {"image": "images/視線の先.jpeg", "title": "視線の先に見える未来", "caption": "P15キャンバス　アクリル絵の具"},
        ],
        "instagram_url": "https://www.instagram.com/kei_kajita"
    },
    "壇奏都": {
        "works": [
            {"image": "images/梅花.jpg", "title": "梅花", "caption": "a6000"},
            {"image": "images/花粉.jpg", "title": "花粉", "caption": "a6000"},
        ],
    },
    "谷本光希": {
        "works": [
            {"image": "images/fruit girl.jpeg", "title": "fruit girl", "caption": "水彩絵の具"},
            {"image": "images/Angel.jpeg", "title": "Angel", "caption": "水彩絵の具"},
        ],
    },
    "杉本結望": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "twitter_url": "https://x.com/oAo_931",
    },
    "五十嵐英奈": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "instagram_url": "https://www.instagram.com/kaaaaro_33?igsh=MWRpeTlkdncxanYyNw%3D%3D&utm_source=qr",
        "twitter_url": "https://x.com/c__krnp?s=21&t=2z1aHpbssmRHgpkBDv5-Xw",
    },
    "波戸優希": {
        "works": [
            {"image": "", "title": "メ・チャ・ミエール", "caption": "Photoshop/Illustrator"},
        ],
        "instagram_url":"https://www.instagram.com/nihonbashi_ukiyo?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==",
        "twitter_url": "https://twitter.com/ukiyo_the_world?s=21&t=FSOIvWDBn5zhbYz-SrY7zQ",
    },
    "山口音寧": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "遠藤胡桃": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "中西祥": {
        "works": [
            {"image": "images/aaa.jpeg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpeg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
}

@app.route("/")
def index():
    author_names = list(authors.keys())
    return render_template("index.html", authors=author_names)

@app.route("/how_to_use")
def how_to_use():
    return render_template("how_to_use.html")

@app.route("/author/<author_name>")
def author(author_name):
    author_data = authors.get(author_name)
    if author_data:
        return render_template("author.html", author_name=author_name, **author_data)
    else:
        abort(404)


@app.route("/work/<author_name>/<int:work_index>")
def work(author_name, work_index):
    author_data = authors.get(author_name)
    if author_data:
        try:
            work_info = author_data["works"][work_index]
            return render_template("work.html", author_name=author_name, work=work_info)
        except IndexError:
            abort(404)
    else:
        abort(404)


# 作品ページへのリダイレクトを追加
@app.route("/work/<author_name>/<int:work_index>")  # 旧URLからのリダイレクト用
def redirect_work(author_name, work_index):
    # work_index をハッシュ化
    work_id = hashlib.md5(str(work_index).encode()).hexdigest()[:4] #短縮化
    return redirect(url_for('work', author_name=author_name, work_id=work_id))



if __name__ == "__main__":
    app.run(debug=True)