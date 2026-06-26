from flask import Flask, request
import requests

from Set_Webhook import set_webh

app = Flask(__name__)

user_state = {}

BOT_TOKEN = "1744473316:V8sHnllCPQBKHRSHDMCi6IDvRmrKIOSQqas"
SEND_MESSAGE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"

WEBHOOK_URL = "https://e01aa7fb4e5f4f.lhr.life/webhook"

set_webh(WEBHOOK_URL)


def ask_llm(text: str):
    """Generate an LLM response."""
    return "it's llm response"


def reports(user_id: int, text: str):
    """Handle user reports."""
    print(f"Report from {user_id}: {text}")


def post_message(payload: dict):
    """Send a request to Bale API."""
    try:
        requests.post(
            SEND_MESSAGE_URL,
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"Send message error: {exc}")


def send_message(chat_id: int, text: str):
    """Send a text message."""
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    post_message(payload)


def send_start_menu(chat_id: int):
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


def send_help(user_id: int):
    """Send help messege"""
    payload = {
        "chat_id": user_id,
        "text": "📖 راهنمای استفاده از RAG Bot\n\n"
        "💬 /ChatMode\n"
        "گفتگو با دستیار هوشمند.\n\n"
        "📝 /Report\n"
        "ثبت باگ، تجربه یا پیشنهاد.\n\n"
        "ℹ️ /About\n"
        "اطلاعات سازنده و پروژه.\n\n"
        "❌ /Exit\n"
        "خروج از حالت گفتگو.\n\n"
        "📚 /Help\n"
        "نمایش این راهنما.",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "/ChatMode", "callback_data": "/ChatMode"}],
                [
                    {
                        "text": "/Rpoert",
                        "callback_data": "/Report",
                    }
                ],
                [
                    {
                        "text": "/About",
                        "callback_data": "/About",
                    }
                ],
                [
                    {
                        "text": "/Exit",
                        "callback_data": "/Exit",
                    }
                ],
                [{"text": "/help", "callback_data": "/help"}],
            ]
        },
    }
    post_message(payload)


def send_about(chat_id: int):
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

    print("New Data:", data)

    text = None
    user_id = None

    if "message" in data:
        text = data["message"].get("text")
        user_id = data["message"]["from"]["id"]

    elif "callback_query" in data:
        text = data["callback_query"].get("data")
        user_id = data["callback_query"]["from"]["id"]

    if text is None or user_id is None:
        return "ok"

    print("User:", user_id)
    print("Text:", text)

    # ---------- Commands ----------

    if text == "/start":
        send_start_menu(user_id)
        return "ok"

    elif text == "/help":
        send_help(user_id)
        return "ok"

    elif text == "/About":
        send_about(user_id)
        return "ok"

    elif text == "/ChatMode":
        user_state[user_id] = "Chat"
        send_message(user_id, "Welcome to Chat Mode!")
        return "ok"

    elif text == "/Report":
        user_state[user_id] = "Report"
        send_message(user_id, "گزارش خود را ارسال کنید.")
        return "ok"

    elif text == "/Exit":
        user_state[user_id] = "Normal"
        send_message(user_id, "از حالت گفتگو خارج شدید.")
        return "ok"

    # ---------- Report Mode ----------

    if user_state.get(user_id) == "Report":
        reports(user_id, text)
        send_message(user_id, "✅ گزارش شما ثبت شد.")
        user_state[user_id] = "Normal"
        return "ok"

    # ---------- Chat Mode ----------

    if user_state.get(user_id) == "Chat":
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
