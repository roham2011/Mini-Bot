from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import ForeignKey 
from .db import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)

    bale_user_id : Mapped[int] = mapped_column(unique=True)

    first_name : Mapped[str | None] = mapped_column()
    
    report_count: Mapped[int] = mapped_column(default=0)
    
class Report(Base):
    __tablename__= "reports"

    def __repr__(self):
        return f"<Report {self.id}: {self.text}>"

    id : Mapped[int] = mapped_column(primary_key=True)

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    text : Mapped[str] = mapped_column()

Base.metadata.create_all(engine)



