from sqlalchemy.orm import Session
from sqlalchemy import select , func
from .models import Report , User

def get_or_save_user(session, user_id, first_name):

    stmt = select(User).where(User.bale_user_id == user_id)

    user = session.scalar(stmt)

    if user is None:
        user = User(bale_user_id=user_id,first_name=first_name)
        session.add(user)

    return user

def save_report(session:Session , user_id:str , text:str):

    report = Report(user_id=user_id , text=text)

    session.add(report)

    return report

def get_all_reports(session:Session , user_id:str):
    
    stmt = select(Report).where(Report.user_id == user_id)

    Data = session.scalars(stmt).all()
    
    return Data

def get_last_report(session:Session , user_id:str):

    stmt = select(Report).Where(Report.user_id == user_id).order_by(Report.id.desc()).limit(1)

    return session.scalar(stmt)