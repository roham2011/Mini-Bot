from utils.send_message import post_message
from Pata_Base.crud import count_reports , get_last_report 

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

def send_count_report(session , user_id : int):
    """this function sends count of user-reports to user."""
    count_report = count_reports(session=session , user_id=user_id)
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

def send_last_report(session , user_id: int):
    las_report = get_last_report(session=session , user_id=user_id)
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
