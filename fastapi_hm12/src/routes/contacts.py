from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_connection_db
from src.repository import contacts as repositories_contacts
from src.schemas import ContactResponse, ContactCreateSchema
from src.entity import ContactsTable, UsersTable
from src.config import logger
from src.services import basic_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_connection_db),
    user:UsersTable=Depends(basic_service.auth_service.get_current_user)
) -> list[ContactsTable]:
    """получить список контактов, привязка к пользователю"""
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
        body: ContactCreateSchema,
        db: AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """создать контакт, привязка к пользователю"""
    contact = await repositories_contacts.create_contact(body, db)
    logger.info(f"contact created with id: {contact.id}")
    return contact

@router.get('/search', response_model=list[ContactResponse])
async def search_contacts(
        first_name:str = Query(None, description='Optional first name to search'),
        last_name:str = Query(None, description='Optional last name to search'),
        email:str = Query(None, description='Optional email to search'),
        db:AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """Поиск контактов по имени, фамили email"""
    if not any([first_name, last_name, email]):
        raise HTTPException(
            status_code=400,
            detail='At least one search parameter must be provided')
    contacts = await repositories_contacts.search_contacts(
        first_name,
        last_name,
        email,
        db)
    
    if not contacts:
        raise HTTPException(status_code=404, detail='Not contacts found')
    return contacts

@router.get('/upcoming_birthdays', response_model=list[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_connection_db),
                             user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """Получить список контактов с датой рождения на 7 дней"""
    upcoming_contacts = await repositories_contacts.get_upcoming_birthdays(db)
    if not upcoming_birthdays:
        raise HTTPException(
            status_code=404,
            detail='No upcoming birthdays within the next 7 days')
    return upcoming_contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_connection_db),
    user: UsersTable = Depends(basic_service.auth_service.get_current_user)
):
    """ получить контакт по id"""
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.put("/{contact_id}")
async def update_contact(
        body: ContactCreateSchema,
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """ Обновить контакт по id"""
    contact = await repositories_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """Удалить контакт по id"""
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact
