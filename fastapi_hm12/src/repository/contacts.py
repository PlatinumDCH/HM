from datetime import datetime, timedelta, date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, or_
from typing import Sequence

from src.entity.models import ContactsTable, UsersTable
from src.schemas import ContactCreateSchema

async def get_contacts(limit: int, offset: int, db: AsyncSession, 
        user: UsersTable)->Sequence[ContactsTable]|None:
    """
    Geting list contacts user limi=? and offset=?
    
    Args:
        limit (int): value contacts with returns in one scope
        offset (int): run before first record/ pagination?
        db (AsyncSession) : async session  curent data base
        user (UsersTable): user who want get contacts

    Returns:
        Sequence[ContactsTable]|None: retuen list of contacts user < limit|offset >
    

    """
    contacts_query = select(ContactsTable).where(
        ContactsTable.users_id==user.id
        ).offset(offset).limit(limit)
    contacts = await db.execute(contacts_query)
    return contacts.scalars().all()

async def get_contact( contact_id: int, db: AsyncSession, 
        user:UsersTable) -> ContactsTable|None :
    """
    Get contact user by id

    Args:
        contact_id (int): id of contact
        db (AsyncSession): async session  curent data base
        user (UsersTable): user who want get contact

    Returns:
        ContactsTable|None: return contact user by id or None if not found
    """
    contact_query = select(ContactsTable).filter_by(id=contact_id,
                                                    users_id=user.id)
    contact = await db.execute(contact_query)
    return contact.scalar_one_or_none()

async def create_contact(body: ContactCreateSchema, db: AsyncSession,
         user:UsersTable)->ContactsTable:
    """
    Create new contact user

    Args:
        body (ContactCreateSchema): data of contact
        db (AsyncSession): async session  curent data base
        user (UsersTable): user who want create contact

    Returns:
        ContactsTable: object ContactsTable
    """
    contact = ContactsTable( **body.model_dump(
                            exclude_unset=True),
                            users_id=user.id) 
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(
        contact_id: int, 
        body: ContactCreateSchema, 
        db: AsyncSession,
        user:UsersTable)->ContactsTable:
    """
    Update contact user by id

    Args:
        contact_id (int): id contact fot search
        body (ContactCreateSchema): data for updater contact
        db (AsyncSession): async session  curent data base
        user (UsersTable): user who want update contact

    Raises:
        HTTPException: wrong contact id

    Returns:
        ContactsTable: contact object ContactsTable
    """
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

async def delete_contact( contact_id: int,db: AsyncSession,
        user:UsersTable)->ContactCreateSchema|None:
    """
        Delete contact by id

        Args:
            contact_id (int): id contact for search
            db (AsyncSession): async session  curent data base
            user (UsersTable): user object table who want delete contact

        Returns:
            ContactCreateSchema|None: deleted obj contact table 
    """
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
    """
        Search contact use parameter

        Args:
            first_name (str): fild table contact
            last_name (str): fild table contact
            email (str): fild table contact
            db (AsyncSession): async session  curent data base
            user (UsersTable): user object 

        Returns:
            Sequence[ContactsTable|None]: finding contact/s
    """
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
        )->list[ContactsTable]:
    """
    Get list contact, birthdays=?

    Args:
        db (AsyncSession): async session  curent data base
        user (UsersTable): user object
        step_days (int, optional): Defaults to 7.

    Returns:
        _type_: list contact/s
    """
    today= datetime.now().date()
    next_week_date = today + timedelta(days=step_days)

    stmt = select(ContactsTable).filter_by(users_id=user.id)
    results = await db.execute(stmt)
    contacts = results.scalars().all()

    upcoming_contacts = [
        contact for contact in contacts
        if today <= replace_year(
            contact.date_birthday, today.year)
            <= next_week_date
    ]

    return upcoming_contacts

def replace_year(date_obj:date, now_year:date)->date:
    """
        Change Y in date -> input Y, учитывая возможность високосного года.

            Args:
                date_obj (date): start date
                now_year (int): needes Y

            Returns:
                date: new date with replase Y. If start date = 29 February,
                    and Y dont is a leap year, return 28 February.

            Raises:
                ValueError: if not isinstanse(start_year, int|float)

            Example:
                ```python
                from datetime import date 

                # Chande Y in simple date
                original_date = date(2020, 3, 1)
                new_date = replace_year(original_date, 2021)
                print(new_date)  # Output: 2021-03-01

                # Change Y in date from February 29 (not a leap year)
                leap_date = date(2020, 2, 29)
                new_leap_date = replace_year(leap_date, 2021)
                print(new_leap_date)  # Output: 2021-02-28
                ```
        """
    try:
        date_python_format = date(date_obj.year, date_obj.month, date_obj.day)
        return date_python_format.replace(year=now_year)
    except ValueError:
        return date_python_format.replace(year=now_year, day=date_obj.day - 1)