from sqlalchemy.orm import Session
from sqlalchemy import select , func
from .models import Report , User , ReportDraft

def get_or_save_user(session:Session, user_id:int, first_name:str):

    stmt = select(User).where(User.bale_user_id == user_id)

    user = session.scalar(stmt)

    if user is None:
        user = User(bale_user_id=user_id,first_name=first_name)
        session.add(user)

    return user

def get_report_draft(session:Session , user_id:int):

    stmt = select(ReportDraft).where(ReportDraft.user_id == user_id)

    draft = session.scalar(stmt)

    return draft

def creat_report_from_draft(session:Session , draft:ReportDraft):

    report = Report(
                    user_id = draft.user_id,
                    title = draft.title,
                    priority = draft.priority,
                    category = draft.category,
                    description = draft.description
                    )
    
    session.add(report)
    session.delete(draft)

    return report

def get_all_reports(session:Session , user_id:int):
    
    stmt = select(Report).where(Report.user_id == user_id)

    Data = session.scalars(stmt).all()
    
    return Data

def get_last_report(session:Session , user_id:int):

    stmt = select(Report).where(Report.user_id == user_id).order_by(Report.id.desc()).limit(1)

    return session.scalar(stmt)