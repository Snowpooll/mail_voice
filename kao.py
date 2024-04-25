import cv2
import time
import configparser
from email_processor import process_email
from gmail_utils import gmail_init

# configparserを使用してINIファイルを読み込む
config = configparser.ConfigParser()
config.read('config.ini')

# 設定を変数に格納
server_ip = config['Settings']['server_ip']
label_id = config['Settings']['label_id']
detection_interval = int(config['Settings']['detection_interval'])

# Haar Cascade分類器の読み込み
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Webカメラの設定
cap = cv2.VideoCapture(0)  # 0番目のカメラを使用する場合

# Gmailサービスの初期化
service = gmail_init()

# 最後の顔検出時刻
lastTime = None

# メインループ
while True:
    # カメラからのフレームの取得
    ret, frame = cap.read()
    
    # フレームのグレースケール化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 顔の検出
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # 検出された顔に対する処理
    for (x, y, w, h) in faces:
        # 検出自の処理（検出から20分たったら再度イベント動かす）
        if lastTime is None or time.perf_counter() - lastTime > detection_interval:
            # 検出時刻更新
            lastTime = time.perf_counter()
            # メール処理関数を呼び出し
            process_email(service, label_id)

# 後処理
cap.release()
cv2.destroyAllWindows()
