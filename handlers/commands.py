def handel_commands(text , bale_user_id , first_name):
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