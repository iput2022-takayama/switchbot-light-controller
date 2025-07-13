import os
import time
import hashlib
import hmac
import base64
import uuid
import requests
import json

# .envファイルから環境変数を読み込む
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ 'dotenv'ライブラリが見つかりません。'pip install python-dotenv' を実行してください。")
    exit()


# 環境変数の取得
TOKEN = os.getenv("SWITCHBOT_TOKEN")
SECRET = os.getenv("SWITCHBOT_SECRET")
DEVICE_ID = os.getenv("SWITCHBOT_DEVICE_ID_COLOR_BULB")

# 環境変数が設定されているかチェック
if not all([TOKEN, SECRET, DEVICE_ID]):
    print("❌ 環境変数 SWITCHBOT_TOKEN, SWITCHBOT_SECRET, SWITCHBOT_DEVICE_ID_COLOR_BULB のいずれかが設定されていません。")
    exit()

# APIリクエストヘッダーの準備
nonce = str(uuid.uuid4())
t = int(round(time.time() * 1000))
string_to_sign = f"{TOKEN}{t}{nonce}".encode("utf-8")
secret = SECRET.encode("utf-8")
sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json; charset=utf8",
    "sign": sign,
    "nonce": nonce,
    "t": str(t),
}

# APIリクエストボディの作成
body = {
    "command": "turnOff",  # ★ コマンドを「オフ」に設定
    "parameter": "default",
    "commandType": "command",
}

# APIエンドポイント
url = f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands"

# APIリクエストの送信
try:
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response.raise_for_status()  # エラーがあれば例外を発生させる
    
    print("✅ コマンド送信成功！ ライトがオフになりましたか？")
    print("レスポンス:", json.dumps(response.json(), indent=2))

except requests.exceptions.RequestException as e:
    print(f"❌ コマンド送信失敗。エラーが発生しました: {e}")
    if e.response:
        print("エラー詳細:", e.response.text)
