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

# ★ APIエンドポイント (ステータス取得用)
url = f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/status"

# --- メインの処理 ---
try:
    print("デバイスの状態を取得します...")
    
    # ★ GETリクエストを送信 (ボディは不要)
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # エラーがあれば例外を発生させる
    
    data = response.json()
    
    print("✅ 状態の取得に成功しました！")
    print("\n--- 受信したレスポンス ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # レスポンスから情報を抽出して分かりやすく表示
    if data.get("body"):
        status = data["body"]
        power = status.get("power", "N/A")
        brightness = status.get("brightness", "N/A")
        color = status.get("color", "N/A")
        color_temp = status.get("colorTemperature", "N/A")

        print("\n--- 解析結果 ---")
        print(f"電源: {power}")
        print(f"明るさ: {brightness}%")
        print(f"色 (R:G:B): {color}")
        print(f"色温度: {color_temp}K")
        print("----------------")

except requests.exceptions.RequestException as e:
    print(f"❌ 状態の取得に失敗しました。エラーが発生しました: {e}")
    if e.response:
        # APIからのエラーメッセージを日本語で補足
        error_data = e.response.json()
        message = error_data.get("message", "")
        if message == "device offline":
            print("エラー詳細: デバイスがオフラインです。ハブとの接続を確認してください。")
        else:
            print("エラー詳細:", e.response.text)
            
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")

