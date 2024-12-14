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
    """получить список контактов, привязка к пользователю  GET
    http://127.0.0.1:8000/api/contacts/?limit=10&offset=0
    barer token: access token
    """
    contacts = await repositories_contacts.get_contacts(limit, offset, db, user)
    return contacts

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
        body: ContactCreateSchema,
        db: AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """
    создать контакт, привязка к пользователю POST
    http://127.0.0.1:8000/api/contacts
    raw JSON :ContactCreateShema 
    auteticate: barer token: access token
    """
    contact = await repositories_contacts.create_contact(body, db, user)
    logger.info(f"contact created with id: {contact.id}")
    return contact

@router.get('/search', response_model=list[ContactResponse])
async def search_contacts(
        first_name:str = Query(None, description='Optional first name to search'),
        last_name:str = Query(None, description='Optional last name to search'),
        email:str = Query(None, description='Optional email to search'),
        db:AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """
    Поиск контактов по first_name, last_name, email  GET
    http://127.0.0.1:8000/api/contacts/search?email=user2
    params: Optional[first_name=X, last_name=X, email=X]
    auteticate: barer token: access token
    """
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
async def upcoming_birthdays(db: AsyncSession = Depends(get_connection_db),
                             user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """
    Получить список контактов с датой рождения на 7 дней  GET
    http://127.0.0.1:8000/api/contacts/upcoming_birthdays
    auteticate: barer token: access token
    """
    upcoming_contacts = await repositories_contacts.get_upcoming_birthdays(db,user)
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
    """
    получить контакт по id  GET
    http://127.0.0.1:8000/api/contacts/6
    auteticate: barer token: access token
    """
    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.put("/{contact_id}")
async def update_contact(
        body: ContactCreateSchema,
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """ 
    Обновить контакт по id PUT
    http://127.0.0.1:8000/api/contacts/6
    raw JSON: ContactCreateShema
    auteticate: barer token: access token
    """
    contact = await repositories_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
        contact_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_connection_db),
        user: UsersTable = Depends(basic_service.auth_service.get_current_user)):
    """
    Удалить контакт по id
    http://127.0.0.1:8000/api/contacts/5
    auteticate: barer token: access token
    """
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    return contact
