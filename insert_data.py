import sqlite3
from models import DB_NAME

# ここに authors のデータを入れる
authors = {
    "内田絢汰": {
        "works": [
            {"image": "images/aaa.jpg" , "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "instagram_url": "https://www.instagram.com/aya___cmr?igsh=MWl1YXY2eW50ejc0bQ%3D%3D&utm_source=qr",
        "twitter_url": "https://x.com/Aya7__Gaming",
    },
    "波多野ひなた": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "instagram_url": "https://www.instagram.com/ultra_happychan?igsh=bmhtZnN0M2hjNGVo&utm_source=qr",
        "twitter_url": "https://x.com/ultra_happychan?s=21&t=toYGO5301kXqijZqUquxQw",
    },
    "戸高花音": {
        "works": [
            {"image": "images/back_side.jpg", "title": "裏側まで", "caption": "デジタル"},
            {"image": "images/cap1.jpg", "title": "", "caption": "Canon EOS kiss X9"},
            {"image": "images/cap2.jpg", "title": "", "caption": "Canon EOS kiss X9"},
            {"image": "images/cap3.jpg", "title": "", "caption": "Canon EOS kiss X9"},
        ],
        "instagram_url": "https://www.instagram.com/oozzz_u_u?igsh=NGc2ejRtMDAzaTV5&utm_source=qr",
    },
    "永井杏奈": {
        "works": [
            {"image": "images/2_blue.jpg", "title": "2人の秘密　真実を隠す子", "caption": "アクリルガッシュ"},
            {"image": "images/2_red.jpg", "title": "2人の秘密　真実を隠す子", "caption": "アクリルガッシュ"},
        ],
        "instagram_url": "https://www.instagram.com/nemunieru_724?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
    },
    "矢野陽菜": {
        "works": [
            {"image": "images/wither.jpg", "title": "末枯れる", "caption": ""},
        ],
    },
    "細谷有未": {
        "works": [
            {"image": "images/A_gorgeous_ballerina1.jpg", "title": "華がある、バレリーナ1", "caption": "写真 スケッチブック ボールペン"},
            {"image": "images/A_gorgeous_ballerina2.jpg", "title": "華がある、バレリーナ2", "caption": "写真 スケッチブック ボールペン"},
            {"image": "images/A_gorgeous_ballerina3.jpg", "title": "華がある、バレリーナ3", "caption": "写真 スケッチブック ボールペン"},
            {"image": "images/city_street1.jpg", "title": "街通り", "caption": "canonEOS80D"},
            {"image": "images/city_street2.jpg", "title": "街通り", "caption": "canonEOS80D"},
            {"image": "images/city_street3.jpg", "title": "街通り", "caption": "canonEOS80D"},
            {"image": "images/city_street4.jpg", "title": "街通り", "caption": "canonEOS80D"},
        ],
        "instagram_url": "https://www.instagram.com/purasu_photo22?igsh=MWZ6dmF3b2NyNzJlMQ%3D%3D&utm_source=qr",
    },
    "石川葵": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "三宅梨菜": {
        "works": [
            {"image": "images/flying.jpg", "title": "飛翔の瞬間", "caption": "CLIP STUDIO PAINT"},
            {"image": "images/creation.jpg", "title": "創造の空間", "caption": "CLIP STUDIO PAINT"},
            {"image": "images/land.jpg", "title": "陸の果てまで歩いた", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/water_lily.jpg", "title": "睡蓮", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/wait.jpg", "title": "待つひと", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/flower_light.jpg", "title": "花明り", "caption": "CLIP STUDIO PAINT"},
            {"image":"images/serenade.jpg", "title": "セレナーデ", "caption": "CLIP STUDIO PAINT"},
        ],
    },
    "川島虹": {
        "works": [
            {"image": "images/gift.jpg", "title": "贈り物", "caption": "水彩、色鉛筆、マルチライナー"},
        ],
    },
    "北村明日香": {
        "works": [
            {"image": "images/sky_breeze.jpg", "title": "空風も和らぐ日", "caption": "OLYMPUS E-M10 MarkⅢ"},
        ],
    },
    "奥村天": {
        "works": [
            {"image": "images/ancient.jpg", "title": "ある古代の一日", "caption": "アクリリックカラー、筆、キャンバス"},
        ],
    },
    "高村咲弥花": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "鍛治美羽": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "西岡愛結": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "梶田恵": {
        "works": [
            {"image": "images/sight.jpg", "title": "視線の先に見える未来", "caption": "P15キャンバス　アクリル絵の具"},
        ],
        "instagram_url": "https://www.instagram.com/kei_kajita"
    },
    "壇奏都": {
        "works": [
            {"image": "images/Plum_blossom.jpg", "title": "梅花", "caption": "a6000"},
            {"image": "images/pollen.jpg", "title": "花粉", "caption": "a6000"},
        ],
    },
    "谷本光希": {
        "works": [
            {"image": "images/fruit_girl.jpg", "title": "fruit girl", "caption": "水彩絵の具"},
            {"image": "images/Angel.jpg", "title": "Angel", "caption": "水彩絵の具"},
        ],
    },
    "杉本結望": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
        "twitter_url": "https://x.com/oAo_931",
    },
    "五十嵐英奈": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
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
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "遠藤胡桃": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
    "中西祥": {
        "works": [
            {"image": "images/aaa.jpg", "title": "空", "caption": "ここはキャプションです"},
            {"image": "images/bbb.jpg", "title": "作品タイトル1-2", "caption": "ここはキャプションです"},
        ],
    },
}

def insert_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # authors を追加
    for name, data in authors.items():
        instagram_url = data.get("instagram_url", None)
        twitter_url = data.get("twitter_url", None)

        cursor.execute("""
        INSERT OR IGNORE INTO authors (name, instagram_url, twitter_url)
        VALUES (?, ?, ?)
        """, (name, instagram_url, twitter_url))

    conn.commit()

    # works を追加
    for name, data in authors.items():
        cursor.execute("SELECT id FROM authors WHERE name = ?", (name,))
        author_id = cursor.fetchone()
        if author_id:
            author_id = author_id[0]
            for work in data["works"]:
                cursor.execute("""
                INSERT INTO works (author_id, image, title, caption)
                VALUES (?, ?, ?, ?)
                """, (author_id, work["image"], work["title"], work["caption"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_data()
    print("データを挿入しました！")
