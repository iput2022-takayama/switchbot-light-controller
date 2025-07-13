import requests
import json
import time
import hashlib
import hmac
import base64
import uuid
import os

# --- .envファイルから環境変数を読み込む ---
from dotenv import load_dotenv
load_dotenv() 

# --- 定数設定 ---
TOKEN = os.getenv("SWITCHBOT_TOKEN")
SECRET = os.getenv("SWITCHBOT_SECRET")
DEVICE_ID = os.getenv("SWITCHBOT_DEVICE_ID_COLOR_BULB") 

# --- ヘッダー生成 ---
def generate_headers():
    """SwitchBot API v1.1用のヘッダーを生成する"""
    nonce = str(uuid.uuid4())
    t = int(round(time.time() * 1000))
    string_to_sign = f'{TOKEN}{t}{nonce}'
    
    sign = base64.b64encode(
        hmac.new(
            SECRET.encode('utf-8'),
            msg=string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
    )

    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
        'charset': 'utf8', # 公式サンプルに合わせて独立したヘッダーにする
        't': str(t),
        'sign': sign.decode('utf-8'),
        'nonce': nonce,
    }
    return headers

# --- メイン処理 ---
def change_color_to_red():
    """電球の色を赤に変更する"""
    api_url = f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands"
    
    headers = generate_headers()
    
    payload = {
        "command": "setColor",
        "parameter": "255:0:0", # RGB: 赤
        "commandType": "command"
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # エラーがあれば例外を発生させる

        # レスポンスボディを解析
        res_body = response.json()
        
        if res_body.get("statusCode") == 100:
            print("✅ コマンド送信成功！ ライトの色は赤に変わりましたか？")
            print("レスポンス:", json.dumps(res_body, indent=2))
        else:
            print("❌ コマンドは送信できましたが、SwitchBot側でエラーが発生しました。")
            print("レスポンス:", json.dumps(res_body, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"❌ APIへのリクエスト中にエラーが発生しました: {e}")
        if e.response:
            print(f"ステータスコード: {e.response.status_code}")
            print(f"レスポンスボディ: {e.response.text}")

if __name__ == "__main__":
    if not all([TOKEN, SECRET, DEVICE_ID]):
        print("❌ 環境変数 SWITCHBOT_TOKEN, SWITCHBOT_SECRET, SWITCHBOT_DEVICE_ID_COLOR_BULB のいずれかが設定されていません。")
    else:
        change_color_to_red()
