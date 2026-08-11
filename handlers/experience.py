from core.enums import UserState, StepResult , ReportCategory , ReportPriority , ExperienceCategory
from sqlalchemy.orm import Session
from database.models import User 
from database.crud import get_report_draft , creat_report_from_draft

def experience_category(session:Session , user:User , text:str):
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

def experience_steps_handler(session:Session , user:User , text:str):
    pass