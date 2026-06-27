from flask import Flask, request
import requests
from Pata_Base.database import reports
from Pata_Base.database import count_reports
from Pata_Base.database import get_last_report
from Set_Webhook import set_webh

app = Flask(__name__)

user_state = {}

TOKEN = "1744473316:V8sHnllCPQBKHRSHDMCi6IDvRmrKIOSQqas"
URL = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

WEBHOOK_URL = "https://e4bfc05017d11a.lhr.life/webhook"

set_webh(WEBHOOK_URL)

def send_user_panel(user_id):
    payload = {
    "chat_id": user_id,
    "text": (
        "سلام به پنل مدیریت کابران خوش آمدید 🌟\n"
        "اگر سوالی دارید، کافی است از ما بپرسید."
    ),
    "reply_markup": {
        "inline_keyboard": [
            [
                {
                    "text": "گفت و گو با مدل زبانی",
                    "callback_data": "/ChatMode",
                }
            ],
            [
                {
                    "text": "درباره ما",
                    "callback_data": "/About",
                }
            ],
                            [
                {
                    "text": "آخرین گزارش شما ",
                    "callback_data": "/LastReport",
                }
            ],
                            [
                {
                    "text": "تعداد تمامی گزارشات",
                    "callback_data": "/CountReports",
                }
            ],
        ]
    },
}
    post_message(payload)

def ask_llm(text: str):
    """Generate an LLM response."""
    return "it's llm response"


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
                        "text": "گفت و گو با مدل زبانی",
                        "callback_data": "/ChatMode",
                    }
                ],
                [
                    {
                        "text": "درباره ما",
                        "callback_data": "/About",
                    }
                ],
                                [
                    {
                        "text": "دیدن پنل کاربری",
                        "callback_data": "/UserPanel",
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
        "گزینه مد نظر خود را نتخاب کنید .\n\n" ,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "/ChatMode", "callback_data": "/ChatMode"}],
                [
                    {
                        "text": "ثبت گزارش",
                        "callback_data": "/Report",
                    }
                ],
                [
                    {
                        "text": "درباره ما",
                        "callback_data": "/About",
                    }
                ],
                [
                    {
                        "text": "خارج شدن از گفت و گو با هوش مصنوعی",
                        "callback_data": "/Exit",
                    }
                ],
                [{"text": "/help", "callback_data": "/help"}],
            ]
        },
    }
    post_message(payload)

def send_help(user_id: int):
    """Send help messege"""
    payload = {
        "chat_id": user_id,
        "text": "📖 راهنمای استفاده از RAG Bot\n\n"
        "گزینه مد نظر خود را نتخاب کنید .\n\n" ,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "/ChatMode", "callback_data": "/ChatMode"}],
                [
                    {
                        "text": "ثبت گزارش",
                        "callback_data": "/Report",
                    }
                ],
                [
                    {
                        "text": "درباره ما",
                        "callback_data": "/About",
                    }
                ],
                [
                    {
                        "text": "خارج شدن از گفت و گو با هوش مصنوعی",
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
def send_count_report(user_id):
    count_report = count_reports(user_id)
    payload = {
    "chat_id": user_id,
    "text": (
        f" تعداد گزارشات شما [{count_report}] بود .\n"
        "اگر سوالی دارید، کافی است از ما بپرسید."
    ),
    "reply_markup": {
        "inline_keyboard": [
            [
                {
                    "text": "گفت و گو با مدل زبانی",
                    "callback_data": "/ChatMode",
                }
            ],
            [
                {
                    "text": "درباره ما",
                    "callback_data": "/About",
                }
            ],
                            [
                {
                    "text": "آخرین گزارش شما ",
                    "callback_data": "/LastReport",
                }
            ]
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
def send_last_report(user_id):
    las_report = get_last_report(user_id)
    payload = {
    "chat_id": user_id,
    "text": (
        f" اخرین گزارش شما [{las_report}] بود .\n"
        "اگر سوالی دارید، کافی است از ما بپرسید."
    ),
    "reply_markup": {
        "inline_keyboard": [
            [
                {
                    "text": "گفت و گو با مدل زبانی",
                    "callback_data": "/ChatMode",
                }
            ],
            [
                {
                    "text": "درباره ما",
                    "callback_data": "/About",
                }
            ],
                            [
                {
                    "text": "تعداد گزارشات شما ",
                    "callback_data": "/CountReport",
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

    # Commands

    if text == "/start":
        send_start_menu(user_id)

        return "ok"

    elif text == "/help":
        send_help(user_id)

        return "ok"

    elif text == "/About":
        send_about(user_id)

        return "ok" 
    
    elif text == "/UserPanel":
        send_user_panel(user_id)

        return "ok"
    
    elif text == "/LastReport":
        send_last_report(user_id)

        return "ok"
    
    elif text == "/CountReport":
        send_count_report(user_id)

        return "ok"
    
    elif text == "/ChatMode":
        user_state[user_id] = "Chat"
        send_message(user_id, "به حالت گفت و گو با هوش مصنویی وارد شدید!")

        return "ok"

    elif text == "/Report":
        user_state[user_id] = "Report"
        send_message(user_id, "گزارش خود را ارسال کنید.")

        return "ok"

    elif text == "/Exit":
        user_state[user_id] = "Normal"
        send_message(user_id, "از حالت گفتگو خارج شدید.")
    
        return "ok"

    # Report Mode

    if user_state.get(user_id) == "Report":
        reports(user_id, text)
        send_message(user_id, "✅ گزارش شما ثبت شد.")
        get_last_report()
        user_state[user_id] = "Normal"

        return "ok"

    # Chat Mode

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
    app.run(debug=True,port=5005,)
