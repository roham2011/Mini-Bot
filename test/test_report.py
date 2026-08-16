from handlers.report import process_steps_report
from database.db import SessionLocal 
from database.models import User
from core.enums import UserState

session = SessionLocal()

user = User()

def test_reports():
    user.current_state = UserState.NORMAL

    resualt = process_steps_report(session=session ,user=user, text="/report")

    assert resualt.message == "عنوان گزارش خویش را وارد کن فرزندم!"


