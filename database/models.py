from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import ForeignKey 
from .db import engine
from datetime import datetime
from core.enums import ReportPriority , UserState

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)

    bale_user_id : Mapped[int] = mapped_column(unique=True)

    first_name : Mapped[str | None] = mapped_column()
    
    report_count: Mapped[int] = mapped_column(default=0)
    
    current_state: Mapped[str] = mapped_column(default=UserState.NORMAL)

class Report(Base):
    __tablename__= "reports"

    def __repr__(self):
        return (
            f"<Report(id={self.id}, "
            f"title={self.title!r})>"
        )

    id : Mapped[int] = mapped_column(primary_key=True)

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    title : Mapped[str] = mapped_column()

    description : Mapped[str] = mapped_column()

    priority : Mapped[str] = mapped_column(default=ReportPriority.MEDIUM)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

Base.metadata.create_all(engine)
