from core.enums import UserState, StepResult , ReportCategory , ReportPriority , ExperienceCategory
from sqlalchemy.orm import Session
from database.models import User , ReportDraft
from database.crud import get_report_draft , creat_report_from_draft

def process_report_title(session:Session , text:str , draft:ReportDraft)-> StepResult | None:
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
    
def process_report_category(session:Session , text:str , draft:ReportDraft)-> StepResult | None:
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

def process_report_priority(session:Session , text:str , draft:ReportDraft)-> StepResult | None:
    draft.priority = ReportPriority(text)

    session.add(draft)

    return StepResult(
        message= "توضیحات گزارش خود را وارد کنید:",
        next_state= UserState.REPORT_DESCRIPTION,
        finished= False
    ) 

def process_report_description(session:Session , text:str , draft:ReportDraft)-> StepResult | None:
    draft.description= text

    session.add(draft)
    creat_report_from_draft(session=session,draft=draft)

    return StepResult(
        message= "گزارش شما ثبت شد.",
        next_state= UserState.NORMAL,
        finished= True
    )

REPORT_STEPS = {
    UserState.REPORT_TITLE: process_report_title,
    UserState.REPORT_CATEGORY: process_report_category,
    UserState.REPORT_PRIORITY: process_report_priority,
    UserState.REPORT_DESCRIPTION: process_report_description,
}

def process_steps_report(text:str , session:Session, user:User ) -> StepResult :
    """this function processes next step in submit report 

    Args:
        text (str): user bot-input
        session (Session): session for manage draft
        user (User): for take user-id and bale-id 

    Returns:
        StepResult: retrun this to specify next step
    """    
    draft = get_report_draft(session=session,user_id=user.id)

    handler = REPORT_STEPS.get(user.current_state)

    if handler is None:
        raise ValueError(f"Invalid report state: {user.current_state}")

    return handler(session=session,text=text,draft=draft) 
