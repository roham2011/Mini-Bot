from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped , mapped_column

class Base(DeclarativeBase):
    pass

class Report(Base):
    __tablename__= "reports"

    id : Mapped[int] = mapped_column(primary_key=True)

    user_id : Mapped[int] = mapped_column()

    text : Mapped[str] = mapped_column()    

