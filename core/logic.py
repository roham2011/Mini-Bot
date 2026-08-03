# include requirement 
from handlers.message import send_about , send_help , send_start_menu , send_user_panel , send_count_report , send_last_report
from handlers.rag.chat import ask_llm
from utils.send_message import send_message
from database.crud import  save_report , get_or_save_user
from database.models import UserState
from .constants import Commands

def handle_messages(session , text:str , bale_user_id:str , first_name:str):
    '''this function returns None and it handels user command'''
     
    user = get_or_save_user(session=session , user_id=bale_user_id , first_name=first_name)

    print("HANDLE:", text)
    print("STATE:", user.current_state)

    command = text.strip().lower()

    if command == Commands.START:
        
        session.commit()

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
        send_last_report(user.bale_user_id)

        return "ok"
    
    if command == Commands.COUNT_REPORT:
        send_count_report(user.bale_user_id , user.report_count)

        return "ok"
    
    if command == Commands.CHAT_MODE:
        user.current_state = UserState.CHAT
        session.commit()

        send_message(user.bale_user_id, "به حالت گفت و گو با هوش مصنویی وارد شدید!")

        return "ok"

    if command == Commands.REPORT:
        user.current_state = UserState.REPORT_DESCRIPTION
        session.commit()

        send_message(user.bale_user_id, "گزارش خود را ارسال کنید.")

        return "ok"

    if command == Commands.EXIT:
        user.current_state = UserState.NORMAL
        session.commit()

        send_message(user.bale_user_id, "از حالت گفتگو خارج شدید.")
    
        return "ok"

    # Chat Mode
    if user.current_state == UserState.CHAT :
        answer = ask_llm(command)
        send_message(user.bale_user_id, answer)

        return "ok"
    return None