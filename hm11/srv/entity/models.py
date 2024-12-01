from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Contact(Base):

    __tablename__                  = 'contact'
    id: Mapped[int]                = mapped_column(primary_key=True,index=True)
    first_name:Mapped[str]         = mapped_column(String(50))
    last_name:Mapped[str]          = mapped_column(String(50))
    email:Mapped[str]              = mapped_column(String(25))
    phone_number:Mapped[str]       = mapped_column(String)
    date_birthday:Mapped[Date]     = mapped_column(Date)
    note:Mapped[str]               = mapped_column(String, default=None)


