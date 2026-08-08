from handlers.rag.report import process_report_step
from database.db import SessionLocal 
from database.models import User
from core.enums import UserState

session = SessionLocal()

user = User()

def test_reports():
    user.current_state = UserState.NORMAL

    resualt = process_report_step(session=session ,user=user, text="/report")

    assert resualt.message == "عنوان گزارش خویش را وارد کن فرزندم!"


