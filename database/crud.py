from sqlalchemy.orm import Session
from sqlalchemy import select , func
from .models import Report , User , ReportDraft ,  ExperienceDraft

def get_or_save_user(session:Session, user_id:int, first_name:str):
    """ this function takes user-data and create object from data (if user is exists returns user)

    Args:
        session (Session): for create and give suser from DB
        user_id (int): for create and give suser from DB with ID
        first_name (str): for سرشث   

    Returns:
        user(object):object afther find or create it  
    """    
    stmt = select(User).where(User.bale_user_id == user_id)

    user = session.scalar(stmt)

    if user is None:
        user = User(bale_user_id=user_id,first_name=first_name)
        session.add(user)

    return user

def get_report_draft(session:Session , user_id:int):
    """this function return report_draft if existed

    Args:
        session (Session): for management dsraft from DB
        user_id (int): for finding Draft from tab 

    Returns:
        draft(object): Draft found
    """    
    stmt = select(ReportDraft).where(ReportDraft.user_id == user_id)

    draft = session.scalar(stmt)

    return draft

def get_exper_draft(session:Session , user_id:int):
    """this function return Exoerience_draft if existed

    Args:
        session (Session): for management draft from DB
        user_id (int): for finding Draft from table

    Returns:
        draft(object): Draft found
    """    
    stmt = select(ExperienceDraft).where(ExperienceDraft.user_id == user_id)

    draft = session.scalar(stmt)

    return draft

def creat_report_from_draft(session:Session , draft:ReportDraft):
    """this function afther create report-draft in wizard adds draft in DB

    Args:
        session (Session): for management draft from DB
        draft (ReportDraft): for add it in DB

    Returns:
        report(object): in fact this is the same Draft
    """    
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