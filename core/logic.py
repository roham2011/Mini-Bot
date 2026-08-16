# include requirement 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from handlers.message import send_about, send_help, send_start_menu, send_user_panel, send_last_report, send_report_count
from database.crud import get_last_report
from handlers.rag.chat import ask_llm
from handlers.report import process_steps_report
from utils.send_message import send_message , post_message
from database.crud import   get_or_save_user
from database.models import UserState , ReportDraft , ExperienceDraft , User
from .constants import Commands
from .enums import ExperienceCategory
# Command Handlers

def handle_start(session: Session, user: User ,text: str):
    user.current_state = UserState.NORMAL

    session.commit()

    send_start_menu(user.bale_user_id,user.first_name)

    return "start-ok"


def handle_help(session: Session, user: User ,text: str):
    send_help(user.bale_user_id)

    return "help-ok"


def handle_about(session: Session, user: User ,text: str):
    send_about(user.bale_user_id)

    return "about-ok"


def handle_user_panel(session: Session, user: User ,text: str):
    send_user_panel(user.bale_user_id)

    return "panel-ok"


def handle_last_report(session: Session, user: User ,text: str):
    report = get_last_report(session,user.id)

    send_last_report(user_id=user.bale_user_id,report=report,)

    return "last-report-ok"


def handle_report_count(session: Session, user: User ,text: str):
    send_report_count(user_id=user.bale_user_id,report_count=user.report_count)

    return "report-count-ok"


def handle_chat_mode(session: Session, user: User ,text: str):
    user.current_state = UserState.CHAT

    session.commit()

    send_message(user.bale_user_id,"به حالت گفت‌وگو با هوش مصنوعی وارد شدید!")

    return "chat-ok"


def handle_report_command(session: Session, user: User ,text: str):
    payload = {
        "chat_id": user.bale_user_id,
        "text": (
            "قصد ثبت گزارش دارید یا تجربه؟\n"
            "یکی از گزینه‌های زیر را انتخاب کنید."
        ),
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "ثبت تجربه",
                        "callback_data": UserState.EXPERIENCE.value,
                    }
                ],
                [
                    {
                        "text": "ثبت گزارش",
                        "callback_data": UserState.REPORT.value,
                    }
                ],
            ]
        },
    }

    post_message(payload)

    return "report-menu-ok"


def handle_report_start(session: Session, user: User ,text: str):
    user.current_state = UserState.REPORT_TITLE

    draft = ReportDraft()
    draft.user_id = user.id

    session.add(draft)
    session.commit()

    send_message(user.bale_user_id,"عنوان گزارش خود را وارد کنید:")

    return "report-start-ok"


def handle_experience_start(session: Session, user: User ,text: str):
    user.current_state = UserState.EXPERIENCE_TITLE

    draft = ExperienceDraft()
    draft.user_id = user.id

    session.add(draft)
    session.commit()

    send_message(user.bale_user_id,"عنوان تجربه خود را وارد کنید:")

    return "experience-start-ok"


def handle_exit(session: Session, user: User ,text: str):
    user.current_state = UserState.NORMAL

    session.commit()

    send_message(user.bale_user_id,"از حالت گفتگو خارج شدید.")

    return "exit-ok"


# State Handler


def handle_state_report(session: Session, user: User ,text: str):
    result = process_steps_report(session=session,user=user, text=text)

    user.current_state = result.next_state

    session.commit()

    if result.keyboard is None:
        send_message(chat_id=user.bale_user_id,text=result.message,)

    else:
        payload = {
            "chat_id": user.bale_user_id,
            "text": result.message,
            "reply_markup": {
                "inline_keyboard": result.keyboard,
            },
        }

        post_message(payload)

    return "state-ok"

def handle_state_experience(session: Session, user: User ,text: str):
    result = process_steps_report(session=session,user=user, text=text)

    user.current_state = result.next_state

    session.commit()

    if result.keyboard is None:
        send_message(chat_id=user.bale_user_id,text=result.message,)

    else:
        payload = {
            "chat_id": user.bale_user_id,
            "text": result.message,
            "reply_markup": {
                "inline_keyboard": result.keyboard,
            },
        }

        post_message(payload)

    return "state-ok"

def handle_chat(session: Session,user: User,text: str,):
    answer = ask_llm(text)

    send_message(
        user.bale_user_id,answer)

    return "chat-message-ok"


# Dictionaries

COMMAND_HANDLERS = {
    Commands.START.lower(): handle_start,
    Commands.HELP.lower(): handle_help,
    Commands.ABOUT.lower(): handle_about,
    Commands.USER_PANEL.lower(): handle_user_panel,
    Commands.LAST_REPORT.lower(): handle_last_report,
    Commands.COUNT_REPORT.lower(): handle_report_count,
    Commands.CHAT_MODE.lower(): handle_chat_mode,
    Commands.REPORT.lower(): handle_report_command,
    Commands.EXIT.lower(): handle_exit,
    # user stats
    UserState.REPORT.value.lower(): handle_report_start,
    UserState.EXPERIENCE.value.lower(): handle_experience_start,
}


# Main Handler

def command_handler(session: Session,text: str,bale_user_id: str,first_name: str):
    try:
        user = get_or_save_user(session=session,user_id=bale_user_id,first_name=first_name)

        print("HANDLE:", text)
        print("STATE:", user.current_state)

        command = text.strip().lower()

        # 1. Commands / callbacks

        handler = COMMAND_HANDLERS.get(command)
        print(f"\n---------------COMMAND--------------- = {command}\n")

        if handler is not None:
            return handler(session=session,user=user,text=text)

        # 2. Report states

        if user.current_state.is_report():
            return handle_state_report(session=session, user=user,text=text)
        
        # 3. Experience states

        if user.current_state.is_experience():
            return handle_state_experience(session=session, user=user,text=text)
        
        # 4. Chat mode

        if user.current_state == UserState.CHAT:
            return handle_chat(session=session,user=user, text=text)

        # 5. Unknown input

        return None

    except SQLAlchemyError as e:
        session.rollback()

        print(f"SQL ERROR: {e}")

        payload = {
            "chat_id": bale_user_id,
            "text": (
                "ربات دچار ایراد فنی شد!\n"
                "یکی از گزینه‌های زیر را انتخاب کنید."
            ),
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "گفت‌وگو با مدل زبانی",
                            "callback_data": Commands.CHAT_MODE,
                        }
                    ],
                    [
                        {
                            "text": "ثبت گزارش",
                            "callback_data": Commands.REPORT,
                        }
                    ],
                    [
                        {
                            "text": "درباره ما",
                            "callback_data": Commands.ABOUT,
                        }
                    ],
                ]
            },
        }

        post_message(payload)

        return "database-error"


