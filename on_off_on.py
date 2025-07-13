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

# APIエンドポイントとヘッダーの準備
url = f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands"

def create_headers():
    """APIリクエスト用のヘッダーを生成する関数"""
    nonce = str(uuid.uuid4())
    t = int(round(time.time() * 1000))
    string_to_sign = f"{TOKEN}{t}{nonce}".encode("utf-8")
    secret = SECRET.encode("utf-8")
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    
    return {
        "Authorization": TOKEN,
        "Content-Type": "application/json; charset=utf8",
        "sign": sign,
        "nonce": nonce,
        "t": str(t),
    }

def send_command(command):
    """指定されたコマンドをSwitchBot APIに送信する関数"""
    headers = create_headers()
    body = {
        "command": command,
        "parameter": "default",
        "commandType": "command",
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response.raise_for_status() # エラーがあれば例外を発生させる
    return response.json()

# --- メインの処理 ---
try:
    # ★ 待ち時間（秒）。この数値を変更すると速さが変わります。
    WAIT_TIME = 0.05 

    # 1. オンにする
    print("1. ライトをオンにします...")
    send_command("turnOn")
    print("✅ オンになりました。")

    # 2. 0.3秒待つ
    time.sleep(WAIT_TIME)

    # 3. オフにする
    print("2. ライトをオフにします...")
    send_command("turnOff")
    print("✅ オフになりました。")

    # 4. 0.3秒待つ
    time.sleep(WAIT_TIME)

    # 5. 再びオンにする
    print("3. ライトを再びオンにします...")
    send_command("turnOn")
    print("✅ 再びオンになりました。")

    # 6. オフにする
    print("2. ライトをオフにします...")
    send_command("turnOff")
    print("✅ オフになりました。")




    # 7. 0.3秒待つ
    time.sleep(WAIT_TIME)

    print("\n🎉 全ての処理が正常に完了しました！")

except requests.exceptions.RequestException as e:
    print(f"❌ コマンド送信失敗。エラーが発生しました: {e}")
    if e.response:
        print("エラー詳細:", e.response.text)

except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
