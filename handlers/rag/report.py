from core.enums import UserState, StepResult
from sqlalchemy.orm import Session
from core.constants import Commands
def process_report_step(text:str , session : Session, user:object):

# define report Conditions here  
  
    if user.current_state == UserState.REPORT_TITLE :

        return StepResult(
            message="عنوان گزارش خویش را وارد کن فرزندم!",
            next_state= UserState.REPORT_TITLE,
            finished= True
        )
        