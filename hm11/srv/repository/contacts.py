from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from datetime import datetime, timedelta, date

from srv.entity.models import Contact, User
from srv.schemas.contacts import ContactCreateSchema

async def get_all_todos(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()

# Получение списка контактов с лимитом и смещением
async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = select(Contact).where(Contact.users_id==user.id).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

# Получение одного контакта по идентификатору
async def get_contact(contact_id: int, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(id=contact_id, users_id=user.id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

# Создание нового контакта
async def create_contact(body: ContactCreateSchema, db: AsyncSession, user:User):
    contact = Contact(**body.model_dump(exclude_unset=True), users_id=user.id)  # (first_name=body.first_name, ...)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

# Обновление существующего контакта
async def update_contact(contact_id: int, body: ContactCreateSchema, db: AsyncSession, user:User):
    stmt = select(Contact).filter_by(id=contact_id, users_id=user.id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contact not found or does not belong to the user'
                            )
    if contact:
        contact.first_name    = body.first_name
        contact.last_name     = body.last_name
        contact.email         = body.email
        contact.phone_number  = body.phone_number
        contact.date_birthday = body.date_birthday
        contact.note          = body.note
        await db.commit()
        await db.refresh(contact)
    return contact

# Удаление контакта
async def delete_contact(contact_id: int, db: AsyncSession, user:User):
    stmt    = select(Contact).filter_by(id=contact_id, users_id=user.id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact

# Поиск контактов по нескольким параметрам
async def search_contacts(
        first_name:str,
        last_name:str,
        email:str,
        db:AsyncSession,
        user: User):
    query = and_(
        Contact.users_id == user.id,
        or_(
        Contact.first_name.like(f'%{first_name}%') if first_name else False,
        Contact.last_name.like(f'%{last_name}%') if last_name else False,
        Contact.email.like(f'%{email}%') if email else False,
              )
    )
    result   = await db.execute(select(Contact).filter(query))
    contacts = result.scalars().all()
    return contacts

# Получение контактов с днями рождения на следующей неделе
async def get_upcoming_birthdays(db:AsyncSession, user:User, step_days : int = 7):
    today          = datetime.now().date()
    next_week_date = today + timedelta(days=step_days)

    #запрос всех контактов из базы данных
    stmt           = select(Contact).filter_by(users_id=user.id)
    results        = await db.execute(stmt)
    contacts       = results.scalars().all()

    # Нахождение контактов с предстоящими днями рождения
    upcoming_contacts = [
        contact for contact in contacts
        if today <= replace_year(
            contact.date_birthday, today.year)
            <= next_week_date
    ]

    return upcoming_contacts

def replace_year(date_obj, new_year):
    try:
        date_python_format = date(date_obj.year, date_obj.month, date_obj.day)
        return date_python_format.replace(year=new_year)
    except ValueError:
        return date(date_obj.year, date_obj.month, date_obj.day-1)