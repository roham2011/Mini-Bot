from flask import Flask, request
# from Pata_Base
from Pata_Base.crud import save_report , get_or_save_user
from Pata_Base.models import User , Report
from Pata_Base.db import SessionLocal
# from utils
from utils.Set_Webhook import set_webh
from utils.send_message import post_message , send_message
# from handlers
from handlers.chat import ask_llm
from handlers.report import send_count_report , send_last_report
# from config
from config import WEBHOOK_URL

app = Flask(__name__)

user_state = {}

set_webh(WEBHOOK_URL)


def send_user_panel(user_id: int):
    """
    this function sends user panel to the user who send "/start" command 
    """
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


def send_start_menu(chat_id: int,first_name:str):
    """Send start menu."""
    payload = {
        "chat_id": chat_id,
        "text": (
            f"سلام {first_name} و خوش آمدید 🌟\n"
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
    message = request.get_json(silent=True) or {}

    print("New Data:", message)

    text = None
    bale_user_id = None
    first_name = None


    if "message" in message:
        text = message["message"].get("text")
        bale_user_id = message["message"]["from"]["id"]
        first_name = message["message"]["from"].get("first_name")
    
    elif "callback_query" in message:
        text = message["callback_query"].get("data")
        bale_user_id = message["callback_query"]["from"]["id"]
        first_name = message["callback_query"]["from"].get("first_name")

    if text is None or bale_user_id is None:
        return "ok"

    print("User:", bale_user_id)
    print("Text:", text)
    
    session = SessionLocal()

    try:
        # Commands
        if text == "/Start":
            user = User(bale_user_id=bale_user_id , first_name=first_name)
            get_or_save_user(session=session , user_id=user.bale_user_id , first_name=user.first_name)
            session.commit()

            send_start_menu(bale_user_id,first_name)

            return "ok"

        elif text == "/help":
            send_help(bale_user_id)

            return "ok"

        elif text == "/About":
            send_about(bale_user_id)

            return "ok" 
        
        elif text == "/UserPanel":
            send_user_panel(bale_user_id)

            return "ok"
        
        elif text == "/LastReport":
            send_last_report(bale_user_id)

            return "ok"
        
        elif text == "/CountReport":
            send_count_report(bale_user_id)

            return "ok"
        
        elif text == "/ChatMode":
            user_state[bale_user_id] = "Chat"
            send_message(bale_user_id, "به حالت گفت و گو با هوش مصنویی وارد شدید!")

            return "ok"

        elif text == "/Report":
            user_state[bale_user_id] = "Report"
            send_message(bale_user_id, "گزارش خود را ارسال کنید.")

            return "ok"

        elif text == "/Exit":
            user_state[bale_user_id] = "Normal"
            send_message(bale_user_id, "از حالت گفتگو خارج شدید.")
        
            return "ok"

        # Report Mode
        if user_state.get(bale_user_id) == "Report":
            save_report(session = session ,user_id = bale_user_id,text = text)
            session.commit()
            
            send_message(bale_user_id, "✅ گزارش شما ثبت شد.")
            
            user_state[bale_user_id] = "Normal"

            return "ok"

        # Chat Mode

        if user_state.get(bale_user_id) == "Chat":
            answer = ask_llm(text)
            send_message(bale_user_id, answer)

            return "ok"
    finally:
        session.close()

    return "ok"


@app.route("/test/<name>")
def test_webhook(name: str):
    """Test route."""
    return f"Hello {name}, webhook is OK!"


if __name__ == "__main__":
    app.run(debug=True,port=5005,)
