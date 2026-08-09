from core.enums import UserState, StepResult
from sqlalchemy.orm import Session
from core.constants import Commands
from database.models import User

def process_report_step(text:str , session : Session, user:User):

# define report Conditions here  
  
    if user.current_state == UserState.REPORT_TITLE :
        
        return StepResult(
            message="عنوان گزارش خویش را وارد کن فرزندم!",
            next_state= UserState.REPORT_CATEGORY,
            finished= False
        )
    if user.current_state == UserState.REPORT_CATEGORY :

        return StepResult(
            message="دسته بندی گزارش خود را وارد کنید :",
            next_state= UserState.REPORT_PRIORITY,
            finished= False
        )
    if user.current_state == UserState.REPORT_PRIORITY :

        return StepResult(
            message="اولیت گزارش خود را انتخاب کنید:",
            next_state= UserState.REPORT_DESCRIPTION ,
            finished= False
        )
    if user.current_state == UserState.REPORT_DESCRIPTION :

        return StepResult(
            message= "توضیحات گزارش خود را وارد کنید:",
            next_state= UserState.NORMAL,
            finished= True 
        )