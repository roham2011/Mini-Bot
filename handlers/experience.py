from core.enums import UserState, StepResult , ReportCategory , ReportPriority , ExperienceCategory
from sqlalchemy.orm import Session
from database.models import User , ExperienceDraft
from database.crud import get_exper_draft , creat_exper_from_draft

def experience_title(session:Session , draft:ExperienceDraft , text:str):
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

def experience_category(session:Session , text:str , draft:ExperienceDraft)-> StepResult | None:
    draft.category = ExperienceCategory(text)

    session.add(draft)

    return StepResult(
        message= "توضیحات تجربه خود را وارد کنید:",
        next_state= UserState.EXPERIENCE_DESCRIPTION,
        finished= False
    ) 

def experience_description(session:Session , text:str , draft:ExperienceDraft)-> StepResult | None:
    draft.description= text

    session.add(draft)
    creat_exper_from_draft(session=session,draft=draft)

    return StepResult(
        message= "تجربه شما ثبت شد.",
        next_state= UserState.NORMAL,
        finished= True
    )

EXPERIENCE_STEPS = {
    UserState.EXPERIENCE_TITLE: experience_title,
    UserState.EXPERIENCE_CATEGORY: experience_category,
    UserState.EXPERIENCE_DESCRIPTION: experience_description,
}

def experience_steps_handler(session:Session , user:User , text:str)-> StepResult :
    """this function processes next step in submit Experience

    Args:
        text (str): user bot-input
        session (Session): session for manage draft
        user (User): for take user-id and bale-id 

    Returns:
        StepResult: retrun this to specify next step
    """    
    draft = get_exper_draft(session=session,user_id=user.id)

    handler = EXPERIENCE_STEPS.get(user.current_state)

    if handler is None:
        raise ValueError(f"Invalid report state: {user.current_state}")

    return handler(session=session,text=text,draft=draft) 