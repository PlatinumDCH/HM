from datetime import datetime, timedelta, date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, or_
from typing import Sequence

from src.entity.models import ContactsTable, UsersTable
from src.schemas import ContactCreateSchema

async def get_contacts(
        limit: int, #количествл контактов за один раз 
        offset: int, #смещение от первой записи
        db: AsyncSession, 
        user:UsersTable
        )->Sequence[ContactsTable]:
    contacts_query = select(ContactsTable).where(
        ContactsTable.users_id==user.id
        ).offset(offset).limit(limit)
    contacts = await db.execute(contacts_query)
    return contacts.scalars().all()

async def get_contact(
        contact_id: int, 
        db: AsyncSession, 
        user:UsersTable) -> ContactsTable|None :
    """получение котакта пользователя по id_contact)"""
    contact_query = select(ContactsTable).filter_by(
        id=contact_id, 
        users_id=user.id
        )
    contact = await db.execute(contact_query)
    return contact.scalar_one_or_none()

async def create_contact(
        body: ContactCreateSchema, 
        db: AsyncSession,
        user:UsersTable)->ContactsTable:
    contact = ContactsTable(
        **body.model_dump(
            exclude_unset=True
            ), users_id=user.id
            ) 
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(
        contact_id: int, 
        body: ContactCreateSchema, 
        db: AsyncSession,
        user:UsersTable)->ContactsTable:
    search_querry = select(ContactsTable).filter_by(id=contact_id, users_id=user.id)
    result = await db.execute(search_querry)
    contact = result.scalar_one_or_none()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    
    contact.first_name = body.first_name
    contact.last_name = body.last_name
    contact.email = body.email
    contact.phone_number = body.phone_number
    contact.date_birthday = body.date_birthday
    contact.note = body.note

    await db.commit()
    await db.refresh(contact)
    return contact

async def delete_contact(
        contact_id: int, 
        db: AsyncSession,
        user:UsersTable):
    search_query = select(ContactsTable).filter_by(id=contact_id, users_id=user.id)
    contact = await db.execute(search_query)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(
        first_name:str,
        last_name:str,
        email:str,
        db:AsyncSession,
        user: UsersTable)->Sequence[ContactsTable|None]:
    query = and_(
        ContactsTable.users_id == user.id,
        or_(
        ContactsTable.first_name.like(f'%{first_name}%') if first_name else False,
        ContactsTable.last_name.like(f'%{last_name}%') if last_name else False,
        ContactsTable.email.like(f'%{email}%') if email else False,
              )
    )
    result   = await db.execute(select(ContactsTable).filter(query))
    contacts = result.scalars().all()
    return contacts


async def get_upcoming_birthdays(
        db:AsyncSession, 
        user:UsersTable, 
        step_days : int = 7,
        ):
    
    today= datetime.now().date()
    next_week_date = today + timedelta(days=step_days)

    stmt           = select(ContactsTable).filter_by(users_id=user.id)
    results        = await db.execute(stmt)
    contacts       = results.scalars().all()

    upcoming_contacts = [
        contact for contact in contacts
        if today <= replace_year(
            contact.date_birthday, today.year)
            <= next_week_date
    ]

    return upcoming_contacts

def replace_year(date_obj:date, now_year:date)->date:

    try:
        date_python_format = date(date_obj.year, date_obj.month, date_obj.day)
        return date_python_format.replace(year=now_year)
    except ValueError:
        return date_python_format.replace(year=now_year, day=date_obj.day - 1)