from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
import unittest

from src.schemas import ContactCreateSchema
from src.entity.models import ContactsTable, UsersTable
from src.repository.contacts import (
                                        get_contacts, 
                                        create_contact, 
                                        update_contact, 
                                        delete_contact, 
                                        get_contact, 
                                        search_contacts, 
                                        get_upcoming_birthdays, 
                                        replace_year
                                        )

class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        starting settings

        User: mock object user
        session: mock object connetion to database
        """
        self.User = UsersTable(id=1,username='test_user', password='123123')
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            ContactsTable(
                id=1, 
                first_name=1, 
                last_name='test_contact1', 
                email='test_email1', 
                phone_number='+380672730962',
                ),
            ContactsTable(
                id=2, 
                first_name=1, 
                last_name='test_contact2', 
                email='test_email2', 
                phone_number='380672730962'
                ),
            ContactsTable(
                id=3, 
                first_name=1, 
                last_name='test_contact3', 
                email='test_email3', 
                phone_number='380672730962'),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.User)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact_id = 2
        mocked_contact = ContactsTable(
            id = contact_id,
            first_name='test_first_name',
            last_name='test_last_name',
            email = 'test@exexmple.com',
            phone_number = '+380672730962',
            date_birthday = '1998-08-01',
            users_id = self.User.id
        )

        mocked_query_results = MagicMock()
        mocked_query_results.scalar_one_or_none.return_value = mocked_contact
        self.session.execute.return_value = mocked_query_results
        result = await get_contact(contact_id, self.session, self.User)
        self.session.execute.assert_called_once()
        self.assertEqual(result, mocked_contact)


    async def test_get_non_existing_contact(self):
        contact_id = 2
        mocked_query_results = MagicMock()
        mocked_query_results.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_query_results
        result = await get_contact(contact_id, self.session, self.User)
        self.session.execute.assert_called_once()
        self.assertIsNone(result)  

    async def test_create_contact(self):
        body = ContactCreateSchema(
            first_name='test_first_name',
            last_name='test_last_name',
            email = 'test@exexmple.com',
            phone_number = '+380672730962',
            date_birthday = '1998-08-01'
        )
        result = await create_contact(body, self.session, self.User)
        self.assertIsInstance(result, ContactsTable)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)


    async def test_update_contact(self):
        body = ContactsTable(
            id=1,
            first_name='test_first_name',
            last_name='test_last_name',
            email = 'test@exexmple.com',
            phone_number = '+380672730962',
            date_birthday = '1998-08-01'
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = ContactsTable(
            id=1,
            first_name='test_first_name',
            last_name='test_last_name',
            email = 'test@exexmple.com',
            phone_number = '+380672730962',
            date_birthday = '1998-08-01'
        )
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.User)
        self.assertIsInstance(result, ContactsTable)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.date_birthday, body.date_birthday)

    async def test_delete_existing_contact(self):
        contact_id = 1
        mocked_contact = ContactsTable(
            id=contact_id,
            first_name='test_first_name',
            last_name='test_last_name',
            email = 'test@exexmple.com',
            phone_number = '+380672730962',
            date_birthday = '1998-08-01',
            users_id=self.User.id
        )

        #mock thre database query
        mocked_contact_query = MagicMock()
        mocked_contact_query.scalar_one_or_none.return_value = mocked_contact
        self.session.execute.return_value = mocked_contact_query

        # call the function 
        result = await delete_contact(contact_id, self.session, self.User)
        
        #vetify the povedenie:

        # check shto response was compleated
        self.session.execute.assert_called_once()
        # check shto contact was deleted
        self.session.delete.assert_called_once_with(mocked_contact)
        # check shto sessiom was closes
        self.session.commit.assert_called_once()
        # check shto function return deleted contact
        self.assertEqual(result, mocked_contact)
    

    async def test_delete_not_existing_contact(self):
        contact_id = 3
        mocked_query_result = MagicMock()
        mocked_query_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_query_result

        # call the function 
        result = await delete_contact(contact_id, self.session, self.User)

        #verify the povedenie
        self.session.execute.assert_called_once()
        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()
        self.assertEqual(result, None)

    async def test_search_contacts(self):
        first_name = 'test'
        last_name = 'test'
        email = 'test@exexmple.com'

        mocked_contacts = [
            ContactsTable(
                id=1,
                first_name='test',
                last_name='test',
                email='test@exexmple.com',
                phone_number='+380672730962',
                date_birthday='1998-08-01',
                users_id=self.User.id
            ),
            ContactsTable(
                id=4,
                first_name='test',
                last_name='test_test',
                email='test@exexmple.com',
                phone_number='+380672730962',
                date_birthday='2000-08-01',
                users_id=self.User.id
            )
        ]

        mocked_query_result = MagicMock()
        mocked_query_result.scalars.return_value.all.return_value = mocked_contacts
        self.session.execute.return_value = mocked_query_result

        result = await search_contacts(
            first_name,
            last_name,
            email,
            self.session,
            self.User
        )

        self.session.execute.assert_called_once()
        self.assertEqual(result, mocked_contacts)

    async def test_search_contacts_no_results(self):
        first_name = 'test'
        last_name = 'test'
        email = 'test@exexmple.com'
        mocked_query_result = MagicMock()
        mocked_query_result.scalars.return_value.all.return_value = []
        self.session.execute.return_value = mocked_query_result
        result = await search_contacts(
            first_name,
            last_name,
            email,
            self.session,
            self.User   
        )
        self.session.execute.assert_called_once()
        self.assertEqual(result, [])
    
    async def test_upcoming_birthdays(self):
        """+7day"""
        today = datetime.now().date()
        mocked_contacts = [
            ContactsTable(
                id=1,
                first_name='test_first',
                last_name='test',
                email='test@exexmple.com',
                phone_number='+380672730962',
                date_birthday=today + timedelta(days=3),
                users_id=self.User.id
            ),
            ContactsTable(
                id=2,
                first_name='test3',
                last_name='test3',
                email='test3@exexmple.com',
                phone_number='+380672730962',
                date_birthday=today + timedelta(days=10),
                users_id=self.User.id
            ),
            ContactsTable(
                id=3,
                first_name='test34',
                last_name='test34',
                email='test34@exexmple.com',
                phone_number='+380672730962',
                date_birthday=today - timedelta(days=5),
                users_id=self.User.id
            )
        ]
        mocked_query_result = MagicMock()
        mocked_query_result.scalars.return_value.all.return_value = mocked_contacts
        self.session.execute.return_value = mocked_query_result

        result = await get_upcoming_birthdays(self.session, self.User)

        self.session.execute.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, 'test_first')

    async def test_get_upcoming_birthdays_not_res(self):
        today = datetime.now().date()
        mocked_contacts = [
            ContactsTable(
                id=1,
                first_name='John',
                last_name='Doe',
                email='john.doe@example.com',
                phone_number='+380672730962',
                date_birthday=today - timedelta(days=5),
                users_id=self.User.id
            ),
            ContactsTable(
                id=2,
                first_name='Jane',
                last_name='Smith',
                email='jane.smith@example.com',
                phone_number='+380672730963',
                date_birthday=today + timedelta(days=10),
                users_id=self.User.id
            ),
        ]
        mocked_query = MagicMock()
        mocked_query.scalars.return_value.all.return_value = mocked_contacts
        self.session.execute.return_value = mocked_query

        result = await get_upcoming_birthdays(self.session, self.User)

        self.session.execute.assert_called_once()
        self.assertEqual(len(result), 0)

    async def test_replace_year_leap_year(self):
        leap_year_birthday = date(2020, 2, 29)
        current_year = 2023
        result = replace_year(leap_year_birthday, current_year)
        self.assertEqual(result, date(2023, 2, 28))

    async def test_replace_year_normal_date(self):
        normal_date = date(2020, 3, 1)
        current_year = 2023
        result = replace_year(normal_date, current_year)
        self.assertEqual(result, date(2023, 3, 1))