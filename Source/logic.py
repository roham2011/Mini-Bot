# include requirement 
from handlers.message import send_about , send_help , send_start_menu , send_user_panel , send_count_report , send_last_report
from handlers.RAG.chat import ask_llm
from utils.send_message import send_message
from Pata_Base.crud import  save_report , get_or_save_user
from Pata_Base.models import UserState

def handle_messages(session , text:str , bale_user_id:str , first_name:str):
     
    user = get_or_save_user(session=session , user_id=bale_user_id , first_name=first_name)

    if text == "/Start":
        
        session.commit()

        send_start_menu(user.bale_user_id , user.first_name)

        return "ok"

    if text == "/help":
        send_help(user.bale_user_id)

        return "ok"

    if text == "/About":
        send_about(user.bale_user_id)

        return "ok" 
    
    if text == "/UserPanel":
        send_user_panel(user.bale_user_id)

        return "ok"
    
    if text == "/LastReport":
        send_last_report(user.bale_user_id)

        return "ok"
    
    if text == "/CountReport":
        send_count_report(user.bale_user_id)

        return "ok"
    
    if text == "/ChatMode":
        user.current_state = UserState.CHAT
        session.commit()

        send_message(user.bale_user_id, "به حالت گفت و گو با هوش مصنویی وارد شدید!")

        return "ok"

    if text == "/Report":
        user.current_state = UserState.REPORT
        session.commit()

        send_message(user.bale_user_id, "گزارش خود را ارسال کنید.")

        return "ok"

    if text == "/Exit":
        user.current_state = UserState.NORMAL
        session.commit()

        send_message(user.bale_user_id, "از حالت گفتگو خارج شدید.")
    
        return "ok"

    # Report Mode
    if user.current_state == UserState.REPORT :
        save_report(session = session ,user_id = user.bale_user_id,text = text)
        session.commit()
        
        send_message(user.bale_user_id, "✅ گزارش شما ثبت شد.")
        
        user.current_state = UserState.NORMAL
        session.commit()
        
        return "ok"

    # Chat Mode
    if user.current_state == UserState.CHAT :
        answer = ask_llm(text)
        send_message(user.bale_user_id, answer)

        return "ok"