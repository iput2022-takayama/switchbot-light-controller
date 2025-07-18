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

# APIエンドポイント
URL = f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands"

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

# ★★★ 変更点：処理時間を計測して返すように関数を修正 ★★★
def send_command(command):
    """指定されたコマンドをSwitchBot APIに送信し、処理時間を計測する関数"""
    headers = create_headers()
    body = {
        "command": command,
        "parameter": "default",
        "commandType": "command",
    }
    
    # --- 時間計測開始 ---
    start_time = time.time()
    
    response = requests.post(URL, headers=headers, data=json.dumps(body))
    response.raise_for_status() # エラーがあれば例外を発生させる
    
    # --- 時間計測終了 ---
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # APIのレスポンスと、かかった時間を返す
    return response.json(), elapsed_time

# --- メインの処理 ---
try:
    # ★ 待ち時間（秒）。この数値を変更すると速さが変わります。
    WAIT_TIME = 0.1
    # ★ 点滅させる回数
    BLINK_COUNT = 3

    print("--- ライトの点滅を開始します ---")

    # 最初に一度だけオンにする
    print("ライトをオンにします...")
    _, elapsed = send_command("turnOn")
    print(f"✅ オンになりました。(所要時間: {elapsed:.4f}秒)")
    time.sleep(WAIT_TIME)

    # 指定した回数だけオフとオンを繰り返す
    for i in range(BLINK_COUNT):
        print(f"\n--- {i + 1}回目の点滅 ---")
        
        # オフにする
        print("ライトをオフにします...")
        _, elapsed_off = send_command("turnOff")
        print(f"✅ オフになりました。(所要時間: {elapsed_off:.4f}秒)")
        time.sleep(WAIT_TIME)

        # オンにする
        print("ライトをオンにします...")
        _, elapsed_on = send_command("turnOn")
        print(f"✅ オンになりました。(所要時間: {elapsed_on:.4f}秒)")
        time.sleep(WAIT_TIME)

    # 最後にオフにする
    print("\nライトをオフにします...")
    _, elapsed_final = send_command("turnOff")
    print(f"✅ オフになりました。(所要時間: {elapsed_final:.4f}秒)")

    print("\n🎉 全ての処理が正常に完了しました！")

except requests.exceptions.RequestException as e:
    print(f"❌ コマンド送信失敗。エラーが発生しました: {e}")
    if e.response:
        print("エラー詳細:", e.response.text)

except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
