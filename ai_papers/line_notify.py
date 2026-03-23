"""LINE Messaging API でプッシュ通知を送信する."""

import os

import requests

LINE_API_URL = "https://api.line.me/v2/bot/message/push"


def send_line_message(message: str) -> None:
    """LINE Messaging APIでプッシュメッセージを送信する."""
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message,
            }
        ],
    }

    resp = requests.post(LINE_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
