import os
import time
import hashlib
import hmac
import base64
import uuid
import requests
import json

# .envファイルから環境変数を安全に読み込む
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ 'dotenv'ライブラリが見つかりません。'pip install python-dotenv' を実行してください。")
    exit()

# 環境変数の取得
TOKEN = os.getenv("SWITCHBOT_TOKEN")
SECRET = os.getenv("SWITCHBOT_SECRET")

# 環境変数が設定されているかチェック
if not all([TOKEN, SECRET]):
    print("❌ 環境変数 SWITCHBOT_TOKEN, SWITCHBOT_SECRET のいずれかが設定されていません。")
    print("   .envファイルに正しく記述されているか確認してください。")
    exit()

# APIリクエストのヘッダーを自動で作るための関数
def generate_headers():
    """SwitchBot APIの認証ヘッダーを生成します"""
    t = int(round(time.time() * 1000))
    nonce = str(uuid.uuid4())
    string_to_sign = f'{TOKEN}{t}{nonce}'
    
    sign = base64.b64encode(
        hmac.new(
            SECRET.encode('utf-8'),
            msg=string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
    )
    
    headers = {
        "Authorization": TOKEN,
        "t": str(t),
        "sign": sign.decode('utf-8'),
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf8"
    }
    return headers

# --- メインの処理 ---
print("SwitchBotサーバーにデバイス一覧を問い合わせています...")

# デバイス一覧を取得するためのAPIのURL
api_url = "https://api.switch-bot.com/v1.1/devices"

try:
    # APIにリクエストを送信
    response = requests.get(api_url, headers=generate_headers())
    response.raise_for_status() # エラーがあればここで例外を発生させる

    # 結果をJSON形式で受け取る
    data = response.json()
    device_list = data.get("body", {}).get("deviceList", [])
    
    # 見やすく表示
    print("✅ デバイス一覧の取得に成功しました！")
    print("\n--- あなたのデバイス一覧 ---")
    if device_list:
        for device in device_list:
            print(f"・デバイス名: {device.get('deviceName', 'N/A')}")
            print(f"  デバイスID: {device.get('deviceId', 'N/A')}")
            print(f"  種類: {device.get('deviceType', 'N/A')}")
            print("-" * 20)
        print("\n操作したいライトの「デバイスID」をコピーして、.envファイルに追記してください。")
        print("例: SWITCHBOT_DEVICE_ID_COLOR_BULB=C1234567890A")
    else:
        print("デバイスが見つかりませんでした。")
    print("--------------------------")

except requests.exceptions.RequestException as e:
    print(f"❌ エラーが発生しました: {e}")
    # エラーの詳細を表示
    if e.response:
        print(f"エラー内容: {e.response.text}")

except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
