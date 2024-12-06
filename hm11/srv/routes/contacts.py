from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.entity.models import User
from srv.repository import contacts as repositories_contacts
from srv.schemas.contacts import ContactCreateSchema, ContactResponse
from srv.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
        limit: int = Query(10, ge=10, le=500),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(auth_service.get_current_user)):
    """ Retrieve a list of contacts with pagination. """
    contacts = await repositories_contacts.get_contacts(limit, offset, db, user)
    return contacts

@router.get('/search', response_model=list[ContactResponse])
async def search_contacts(
        first_name:str = Query(None, description='Optional first name to search'),
        last_name:str = Query(None, description='Optional last name to search'),
        email:str = Query(None, description='Optional email to search'),
        db:AsyncSession = Depends(get_db),
        user: User = Depends(auth_service.get_current_user)):
    """Search for contacts by first name, last name, or email. """
    if not any([first_name, last_name, email]):
        raise HTTPException(
            status_code=400,
            detail='At least one search parameter must be provided')
    contacts = await repositories_contacts.search_contacts(
        first_name,
        last_name,
        email,
        db,
        user)

    if not contacts:
        raise HTTPException(status_code=404, detail='Not contacts found')
    return contacts

@router.get('/upcoming_birthdays', response_model=list[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db),
                             user: User = Depends(auth_service.get_current_user)):
    """ Retrieve contacts with upcoming birthdays within the next 7 days. """
    upcoming_contacts = await repositories_contacts.get_upcoming_birthdays(db,user)
    if not upcoming_birthdays:
        raise HTTPException(
            status_code=404,
            detail='No upcoming birthdays within the next 7 days')
    return upcoming_contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(auth_service.get_current_user)):
    """ Get contact object from database """
    contact = await repositories_contacts.get_contact(contact_id, db,user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND")
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
        body: ContactCreateSchema,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(auth_service.get_current_user)):
    """ Create contact object """
    contact = await repositories_contacts.create_contact(body, db,user)
    return contact

@router.put("/{contact_id}")
async def update_contact(
        body: ContactCreateSchema,
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(auth_service.get_current_user)):
    """ Update contact object"""
    contact = await repositories_contacts.update_contact(contact_id, body, db,user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    return contact

