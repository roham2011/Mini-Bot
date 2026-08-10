from core.enums import UserState, StepResult , ReportCategory , ReportPriority , ExperienceCategory
from sqlalchemy.orm import Session
from database.models import User 
from database.crud import get_report_draft , creat_report_from_draft

def process_report_or_exper(text:str , session:Session, user:User ):
    """this function processes next step in submit report and submit Experience

    Args:
        text (str): user bot-input
        session (Session): session for manage draft
        user (User): for take user-id and bale-id 

    Returns:
        StepResult: retrun this to specify next step
    """    
    # define report Conditions here
    if user.current_state == UserState.REPORT:

        user.current_state = UserState.REPORT_TITLE

        if user.current_state == UserState.REPORT_TITLE:
            draft = get_report_draft(session=session , user_id=user.id)
            draft.title = text

            session.add(draft)
            return StepResult(
                message="دسته بندی گزارش خود را وارد کنید :",
                next_state= UserState.REPORT_CATEGORY,
                finished= False,
                keyboard=[
                            [
                                {"text": "خرابی", "callback_data": ReportCategory.BREAKDOWN.value},
                                {"text": "ارور", "callback_data": ReportCategory.ERROR.value},
                                {"text": "متفرقه", "callback_data": ReportCategory.OTHER.value}
                            ]
                        ]) 

        if user.current_state == UserState.REPORT_CATEGORY  :
            draft.category = ReportCategory(text)
            session.add(draft)

            return StepResult(
                message="اولیت گزارش خود را انتخاب کنید:",
                next_state= UserState.REPORT_PRIORITY ,
                finished= False,
                keyboard=[
                            [
                                {"text": "اولیت پایین", "callback_data": ReportPriority.LOW.value},
                                {"text": "الویت متوسط", "callback_data": ReportPriority.MEDIUM.value},
                                {"text": "اولیت بالا", "callback_data":  ReportPriority.HIGH.value},
                                {"text": "بحرانی", "callback_data": ReportPriority.CRITICAL.value}
                            ]
                        ])
            
        if user.current_state == UserState.REPORT_PRIORITY :
            draft.priority = ReportPriority(text)

            session.add(draft)

            return StepResult(
                message= "توضیحات گزارش خود را وارد کنید:",
                next_state= UserState.REPORT_DESCRIPTION,
                finished= False
            ) 
        
        if user.current_state == UserState.REPORT_DESCRIPTION :
            draft.description= text

            session.add(draft)
            creat_report_from_draft(session=session,draft=draft)

            return StepResult(
                message= "گزارش شما ثبت شد.",
                next_state= UserState.NORMAL,
                finished= True
            )
    else :
        user.current_state = UserState.EXPERIENCE_TITLE

        if user.current_state == UserState.EXPERIENCE_TITLE:
            draft = get_report_draft(session=session , user_id=user.id)
            draft.title = text

            session.add(draft)
            return StepResult(
                message="دسته بندی تجربه خود را وارد کنید :",
                next_state= UserState.EXPERIENCE_CATEGORY,
                finished= False,
                keyboard=[
                            [
                                {"text": "نوآوری", "callback_data": ExperienceCategory.INNOVATION.value},
                                {"text": "ایده", "callback_data": ExperienceCategory.IDEA.value},
                                {"text": "حل خطا", "callback_data": ExperienceCategory.DEBUGING.value},
                                {"text": "متفرقه", "callback_data": ExperienceCategory.OTHER.value}
                            ]
                        ]) 
