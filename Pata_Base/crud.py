from sqlalchemy.orm import Session , sessionmaker 
from sqlalchemy import select 
from db import engine
from models import Report , User

def save_report(session:Session , user_id:str , text:str):
    report = Report(user_id=user_id , text=text)

    session.add(report)
    session.commit()

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