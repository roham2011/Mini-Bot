from database.models import UserState
from core.resualts import step_resualts
from sqlalchemy.orm import Session

def process_report_step(text:str , session : Session, ):

    return step_resualts()