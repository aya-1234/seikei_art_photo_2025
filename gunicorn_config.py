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

# ワーカープロセスの最大リクエスト数
max_requests = 1000  # 各ワーカーが最大1000リクエスト処理後にリスタート

# 最大リクエスト後のジッター（ランダムな時間）
max_requests_jitter = 50  # ジッターによってワーカーの再起動タイミングを少しずらす

# プリロードの設定（パフォーマンス最適化のため）
preload_app = True  # Trueの場合、アプリを最初にロードし、ワーカーがそれを使用

# リソース制限（メモリ・CPU制限）
worker_tmp_dir = '/tmp'  # ワーカーの一時ファイル格納場所