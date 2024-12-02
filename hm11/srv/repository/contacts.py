from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime, timedelta

from srv.entity.models import Contact
from srv.schemas.contacts import ContactCreateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactCreateSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))  # (title=body.title, description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactCreateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.date_birthday = body.date_birthday
        contact.note = body.note
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact

async def search_contacts(
        first_name:str,
        last_name:str,
        email:str,
        db:AsyncSession ):
    query = or_(
        Contact.first_name.like(f'%{first_name}%') if first_name else False,
        Contact.last_name.like(f'%{last_name}%') if last_name else False,
        Contact.email_name.like(f'%{email}%') if email else False,
              )
    result = await db.execute(select(Contact).filter(query))
    contacts = result.scalars().all()
    return contacts

async def get_upcoming_birthdays(db:AsyncSession):
    today = datetime.now().date()
    next_week_date = today + timedelta(days=7)
    results = await db.execute(select(Contact))
    contacts = results.scalars().all()

    upcoming_contacts = [
        contact for contact in contacts
        if today <= contact.date_birthday.replace(
            year=today.year) <= next_week_date
    ]

    return upcoming_contacts