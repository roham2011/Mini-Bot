from config import URL
import requests

def post_message(payload: dict):
    """Send a request to Bale API."""
    try:
        requests.post(
            URL,
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"Send message error: {exc}")

def send_message(chat_id: int, text: str):
    """this function sends message to user."""
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    post_message(payload)