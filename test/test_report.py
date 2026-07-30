from handlers.rag.report import process_report_step
from database.db import SessionLocal 

session = SessionLocal

def tset_reports():
    resualt = process_report_step(session=session , text="/report")
    assert process_report_step()