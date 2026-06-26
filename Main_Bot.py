from flask import Flask, request
import requests

from Set_Webhook import set_webh

app = Flask(__name__)

user_state = {}

BOT_TOKEN = "YOUR_TOKEN"
SEND_MESSAGE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"

WEBHOOK_URL = "https://97eabdd3e26e80.lhr.life/webhook"

set_webh(WEBHOOK_URL)


def ask_llm(text: str) -> str:
    """Generate an LLM response."""
    return "it's llm response"


def reports(user_id: int, text: str) -> None:
    """Handle user reports."""
    print(f"Report from {user_id}: {text}")


def post_message(payload: dict) -> None:
    """Send a request to Bale API."""
    try:
        requests.post(
            SEND_MESSAGE_URL,
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"Send message error: {exc}")


def send_message(chat_id: int, text: str) -> None:
    """Send a text message."""
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    post_message(payload)


def send_start_menu(chat_id: int) -> None:
    """Send start menu."""
    payload = {
        "chat_id": chat_id,
        "text": (
            "سلام و خوش آمدید 🌟\n"
            "به ربات ما خوش آمدید! خوشحالیم که اینجا هستید 😊\n"
            "اگر سوالی دارید، کافی است از ما بپرسید."
        ),
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "/ChatMode",
                        "callback_data": "/ChatMode",
                    }
                ],
                [
                    {
                        "text": "/About",
                        "callback_data": "/About",
                    }
                ],
            ]
        },
    }

    post_message(payload)


def send_about(chat_id: int) -> None:
    """Send about message."""
    payload = {
        "chat_id": chat_id,
        "text": 'This Bot was developed by "Roham".',
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "/ChatMode",
                        "callback_data": "/ChatMode",
                    }
                ]
            ]
        },
    }

    post_message(payload)


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle Bale webhook requests."""
    data = request.get_json(silent=True) or {}

    text = None
    user_id = None

    print("**New Data**", data)

    if "message" in data:
        text = data["message"].get("text")
        user_id = data["message"]["from"]["id"]

    elif "callback_query" in data:
        text = data["callback_query"].get("data")
        user_id = data["callback_query"]["from"]["id"]

    elif not text or user_id is None:
        pass

    elif text == "/ChatMode":
        user_state[user_id] = "Chat"
        send_message(user_id, "Welcome to ChatMode!")

    elif text == "/Exit":
        user_state[user_id] = "Normal"
        send_message(user_id, "Welcome to Normal Mode!")

    elif text == "/Start":
        send_start_menu(user_id)

    elif text == "/About":
        send_about(user_id)

    elif text == "/Report":
        user_state[user_id] = "Report"
        send_message(user_id, "Submit your report.")

    elif user_state.get(user_id) == "Report":
        reports(user_id, text)
        send_message(user_id, "Report received.")
        user_state[user_id] = "Normal"

    elif user_state.get(user_id) == "Chat":
        answer = ask_llm(text)
        send_message(user_id, answer)
        return "ok"
    return "ok"


@app.route("/test/<name>")
def test_webhook(name: str):
    """Test route."""
    return f"Hello {name}, webhook is OK!"


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001,
    )
