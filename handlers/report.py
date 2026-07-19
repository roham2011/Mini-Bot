from utils.send_message import post_message
from Pata_Base.crud import count_reports , get_last_report

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
