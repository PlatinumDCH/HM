from datetime import date
import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, func, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__               = 'contact'
    id: Mapped[int]             = mapped_column(primary_key=True,index=True)
    first_name:Mapped[str]      = mapped_column(String(50))
    last_name:Mapped[str]       = mapped_column(String(50))
    email:Mapped[str]           = mapped_column(String(25))
    phone_number:Mapped[str]    = mapped_column(String)
    date_birthday:Mapped[Date]  = mapped_column(Date)
    note:Mapped[str]            = mapped_column(String, default=None)
    created_at: Mapped[date]    = mapped_column('created_at',DateTime,default=func.now(),
                                nullable=True)
    updated_at: Mapped[date]    = mapped_column('updated_at',DateTime,default=func.now(),
                                onupdate=func.now(),nullable=True)
    users_id: Mapped[int]       = mapped_column(Integer,ForeignKey('users.id'),nullable=True)
    user: Mapped['User']        = relationship('User', backref='todos', lazy='joined')

class Role(enum.Enum):
    admin: str     = "admin"
    moderator: str = "moderator"
    user: str      = "user"

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int]          = mapped_column(primary_key=True)
    username: Mapped[str]    = mapped_column(String(50))
    email: Mapped[str]       = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str]    = mapped_column(String(255), nullable=False)
    avatar: Mapped[str]      = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(),
                                             onupdate=func.now())
    role: Mapped[Enum] = mapped_column('role', Enum(Role), default=Role.user, nullable=True)

class UserToken(Base):
    __tablename__              = 'user_token'
    id: Mapped[int]            = mapped_column(primary_key=True,index=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int]       = mapped_column(Integer, ForeignKey('users.id'),nullable=False)
    user: Mapped['User']       = relationship('User', backref='tokens',lazy='joined')