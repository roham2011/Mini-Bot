from core.enums import UserState, StepResult , ReportCategory , ReportPriority , ExperienceCategory
from sqlalchemy.orm import Session
from database.models import User 
from database.crud import get_report_draft , creat_report_from_draft

def handle_submission_title(text: str, session:Session, user:User) -> StepResult:
    draft = get_report_draft(session=session , user_id=user.id)
    




def process_report_or_exper(text:str, session:Session, user:User ) -> StepResult:
    handlers = {}