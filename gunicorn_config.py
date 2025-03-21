import multiprocessing

# ワーカーの数（CPUコア数に合わせるのが一般的）
workers = multiprocessing.cpu_count() * 2 + 1

# ソケットファイルのパス
bind = 'unix:/var/www/seikei_art_photo_2025/seikei_art_photo_2025.sock'

# タイムアウト時間（秒）
timeout = 300

# ログの設定（任意）
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

# ワーカーのタイプ
worker_class = 'sync'  # 通常の同期ワーカー（変更可