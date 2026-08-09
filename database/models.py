from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy import ForeignKey 
from .db import engine
from datetime import datetime
from core.enums import ReportPriority , Category ,UserState
from sqlalchemy import Enum as SQLEnum

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)

    bale_user_id : Mapped[int] = mapped_column(unique=True)

    first_name : Mapped[str | None] = mapped_column()
    
    report_count : Mapped[int] = mapped_column(default=0)
    
    current_state : Mapped[UserState] = mapped_column(SQLEnum(UserState),default=UserState.NORMAL)

    report : Mapped[list["Report"]] = relationship(back_populates="user")


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

    category : Mapped[Category] = mapped_column(SQLEnum(Category),default=Category.OTHER)

    priority : Mapped[ReportPriority] = mapped_column(SQLEnum(ReportPriority),default=ReportPriority.UNKNOWN)
    
    created_at : Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user : Mapped["User"] = relationship(back_populates="report")


class ReportDraft(Base):
    __tablename__ = "report_drafts"
    def __repr__(self):
        return (f"<draft Report\n- (user_id={self.user_id})\n"
                f"- (title={self.title})\n"
                f"- (category={self.category})\n"
                f"- (priority={self.priority})\n"
                f"- (description={self.description})>")
    
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    title : Mapped[str | None] = mapped_column()

    category : Mapped[Category | None] = mapped_column(SQLEnum(Category))

    description : Mapped[str | None] = mapped_column()

    priority : Mapped[ReportPriority | None] = mapped_column(SQLEnum(ReportPriority))
    
Base.metadata.create_all(engine)
