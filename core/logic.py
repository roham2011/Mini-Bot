# include requirement 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from handlers.message import send_about, send_help, send_start_menu, send_user_panel, send_last_report, send_report_count
from database.crud import get_last_report
from handlers.rag.chat import ask_llm
from handlers.rag.report import process_report_or_exper
from utils.send_message import send_message , post_message
from database.crud import   get_or_save_user
from database.models import UserState , ReportDraft , ExperienceDraft
from .constants import Commands
from .enums import ExperienceCategory
def handle_messages(session:Session , text:str , bale_user_id:str , first_name:str):
    """this function returns None and it handels user command

    Args:
        session (Session): for manage data
        text (str): user-input for handle response
        bale_user_id (str): for post message to user and creat User-object
        first_name (str): for creat User-object

    Returns:
        str(OK): for confirm
    """    


    try:
        user = get_or_save_user(session=session , user_id=bale_user_id , first_name=first_name)

        print("HANDLE:", text)
        print("STATE:", user.current_state)

        command = text.strip().lower()

        if command == Commands.START:
            
            session.commit()
            user.current_state = UserState.NORMAL
            send_start_menu(user.bale_user_id , user.first_name)

            print("START MENU SENT")

            return "ok"

        if command == Commands.HELP:
            send_help(user.bale_user_id)

            return "ok"

        if command == Commands.ABOUT:
            send_about(user.bale_user_id)

            return "ok" 
        
        if command == Commands.USER_PANEL:
            send_user_panel(user.bale_user_id)

            return "ok"
        
        if command == Commands.LAST_REPORT:
            report = get_last_report(session, user.id)

            send_last_report(user_id=user.bale_user_id,report=report)

            return "ok"
            
        if command == Commands.COUNT_REPORT:
            send_report_count(user_id=user.bale_user_id,report_count=user.report_count)

            return "ok"
        
        if command == Commands.CHAT_MODE:
            user.current_state = UserState.CHAT
            session.commit()

            send_message(user.bale_user_id, "به حالت گفت و گو با هوش مصنویی وارد شدید!")

            return "ok"
        
        if command == Commands.REPORT:

            payload = {
                "chat_id": user.bale_user_id,
                "text": (
                        "قصد ثبت گزارش دارید یا تجربه ؟\n"
                        "یکی از گزینه‌های زیر را انتخاب کنید."
                ),
                "reply_markup": {
                "inline_keyboard": [
                    [{"text": "ثبت تجربه", "callback_data": UserState.EXPERIENCE.value}],
                    [{"text": "ثبت گزارش", "callback_data": UserState.REPORT.value}]
                ]
                },
            }

            post_message(payload)
            return "ok" 
        
        if text == UserState.REPORT.value:
            user.current_state = UserState.REPORT
            draft = ReportDraft()
            draft.user_id = user.id
            session.add(draft)
            session.commit()

            send_message(user.bale_user_id,"عنوان گزارش خود را وارد کنید:")

            return "ok"

        if text == UserState.EXPERIENCE.value:
            user.current_state = UserState.EXPERIENCE
            draft = ExperienceDraft()
            draft.user_id = user.id
            session.add(draft)
            session.commit()

            send_message(user.bale_user_id, "عنوان تجربه خود را وارد کنید:")

            return "ok"
    
        if command == Commands.EXIT:
            user.current_state = UserState.NORMAL
            session.commit()

            send_message(user.bale_user_id, "از حالت گفتگو خارج شدید.")
        
            return "ok"

        if user.current_state.not_normal_or_chat():
            user.current_state = text
            result = process_report_or_exper(
                session=session,
                user=user,
                text=text,
            )
            user.current_state = result.next_state
            session.commit()

            if result.keyboard == None :
                send_message(chat_id=user.bale_user_id,text=result.message)

            if result.keyboard != None :
                payload = {
                    "chat_id": user.bale_user_id,
                    "text": (
                            result.message
                    ),
                    "reply_markup": {
                        "inline_keyboard": result.keyboard
                    },
                }

                post_message(payload)

        # Chat-Mode
        if user.current_state == UserState.CHAT :
            answer = ask_llm(command)
            send_message(user.bale_user_id, answer)

            return "ok"
        return None
    
    except SQLAlchemyError as e:
        session.rollback()

        print(f"SQL ERROR ! :{e}")

        payload = {
            "chat_id": user.bale_user_id,
            "text": (
                    "بازو دچار ایراد فنی شد!\n"
                    "یکی از گزینه‌های زیر را انتخاب کنید."
            ),
            "reply_markup": {
            "inline_keyboard": [
                [{"text": "گفت‌وگو با مدل زبانی", "callback_data": Commands.CHAT_MODE}],
                [{"text": "ثبت گزارش", "callback_data": Commands.REPORT}],
                [{"text": "درباره ما", "callback_data": Commands.ABOUT}]
            ]
            },
        }

        post_message(payload)

        return "ok"