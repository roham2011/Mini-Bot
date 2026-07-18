from sqlalchemy.orm import Session
from sqlalchemy import select 
from .db import engine
from .models import Report , User

def get_or_save_user(session:Session , user_id:str , first_name:str):

    user = User(bale_user_id=user_id , first_name=first_name)

    stmt = select(User).where(User.bale_user_id == user_id)
    user = session.scalar(stmt)

    if user is None :
        user = User(bale_user_id=user_id , first_name=first_name)
        session.add(user)
    else :
        return user
    
    return user

def save_report(session:Session , user_id:str , text:str):

    report = Report(user_id=user_id , text=text)

    session.add(report)

    return report

def get_all_reports(session:Session , user_id:str):
    
    stmt = select(Report).where(Report.user_id == user_id)

    Data = session.scalars(stmt).all()
    
    return Data

"""SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

user1 = User(user_id = 93480 , first_name = "Reham")

session.add(user1)
session.commit()

report1 = save_report(session = session,user_id = user1.id , text = "Helo")

last_rep1 = get_all_reports(session = session,user_id = user1.id)

print (last_rep1)

session.close()"""