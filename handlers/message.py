from utils.send_message import post_message
from core.constants import Commands


def send_start_menu(chat_id: int, first_name: str):
    payload = {
        "chat_id": chat_id,
        "text": (
            f"سلام {first_name}، خوش آمدید 🌟\n"
            "خوشحالیم که اینجا هستید 😊\n"
            "اگر سوالی دارید، کافی است از ما بپرسید."
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "گفت‌وگو با مدل زبانی", "callback_data": Commands.CHAT_MODE}],
                [{"text": "درباره ما", "callback_data": Commands.ABOUT}],
                [{"text": "پنل کاربری", "callback_data": Commands.USER_PANEL}],
            ]
        },
    }

    post_message(payload)


def send_user_panel(user_id: int):
    payload = {
        "chat_id": user_id,
        "text": "به پنل کاربری خوش آمدید.",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "گفت‌وگو با مدل زبانی", "callback_data": Commands.CHAT_MODE}],
                [{"text": "آخرین گزارش", "callback_data": Commands.LAST_REPORT}],
                [{"text": "تعداد گزارش‌ها", "callback_data": Commands.COUNT_REPORT}],
                [{"text": "درباره ما", "callback_data": Commands.ABOUT}],
            ]
        },
    }

    post_message(payload)


def send_help(user_id: int):
    payload = {
        "chat_id": user_id,
        "text": (
            "📖 راهنمای استفاده\n\n"
            "یکی از گزینه‌های زیر را انتخاب کنید."
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "گفت‌وگو با مدل زبانی", "callback_data": Commands.CHAT_MODE}],
                [{"text": "ثبت گزارش", "callback_data": Commands.REPORT}],
                [{"text": "درباره ما", "callback_data": Commands.ABOUT}],
                [{"text": "خروج", "callback_data": Commands.EXIT}],
            ]
        },
    }

    post_message(payload)


def send_about(user_id: int):
    payload = {
        "chat_id": user_id,
        "text": "This bot was developed by Roham.",
    }

    post_message(payload)


def send_report_count(user_id: int, report_count: int):
    payload = {
        "chat_id": user_id,
        "text": f"تعداد گزارش‌های شما: {report_count}",
    }

    post_message(payload)


def send_last_report(user_id: int, report):
    """
    report can be a database object or None (since it might not exist)
    """

    if report is None:
        text = "شما هنوز گزارشی ثبت نکرده‌اید."
    else:
        text = (
            f"📝 آخرین گزارش شما\n\n"
            f"عنوان: {report.title}\n"
            f"اولویت: {report.priority}\n\n"
            f"{report.description}"
        )

    payload = {
        "chat_id": user_id,
        "text": text,
    }

    post_message(payload)