import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserResponse
from src.entity.models import UsersTable, UserTokensTable
from src.schemas import UserSchema
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    get_token,
    confirmed_email,
    update_user_password,
    update_avatar_url,
)

test_cases = {
    "update_token": [
        "test_update_token_success",
        "test_update_token_NoneVal",
        "test_update_token_db_err",
    ],
    "get_token": [
        "test_get_token",
        "test_get_token_not_found",
        "test_get_token_invalid_token",
        "test_get_token_db_error",
    ],
    "get_user_by_email": [
        "test_get_user_by_email",
    ],
    "create_user": [
        "test_create_user_success",
        "create_user_avatar_error",
    ],
    "confirmed_email": [
        "test_confirmed_user_email",
    ],
    "update_user_password": [
        "test_update_user_password",
    ],
    "update_avatar_url": [
        "test_update_avatar_url",
    ],
}


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.new_password = "new_password"
        cls.new_graw_url = "https://www.exemple.com/avatar/mocked_avatar_url"
        cls.new_token_value = "new_token_value"
        cls.token_type = "refresh_token"
        cls.email = 'test@gmail.com'

    def setUp(self):

        self.session = AsyncMock(spec=AsyncSession)

        self.user = UsersTable(
            id=2,
            username="test_user",
            password="password",
            email="test@gmail.com",
            confirmed=False,
            avatar=None,
        )

        self.user_token = UserTokensTable(
            user_id=self.user.id,
            refresh_token="refresh_token_value",
            reset_password_token="reset_password_token_value",
            email_token="email_token_value",
        )
        self.test_body = UserSchema(
            email="test@gmail.com", 
            password="password", 
            username="test_user"
        )

        

    @patch("src.repository.users.select")
    @patch("src.repository.users.update")
    async def test_update_token_success(self, mock_update, mock_select):
        """suncesfull updating token_value->new_token_value"""
        # settings mock for select
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )

        # settigns mock for execute
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.user_token
        self.session.execute.return_value = mock_result

        # settings мock for update
        mock_update.return_value = update(UserTokensTable).where(
            UserTokensTable.user_id == self.user.id
        )

        await update_token(
            user=self.user,
            token=self.new_token_value,
            token_type=self.token_type,
            db=self.session,
        )

        self.assertEqual(self.user_token.refresh_token, self.new_token_value)
        self.session.execute.assert_called()
        self.assertEqual(self.session.execute.call_count, 2)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    @patch("src.repository.users.select")
    @patch("src.repository.users.update")
    async def test_update_token_NoneVal(self, mock_update, mock_select):
        """upgrade token_values -> None <delete>"""
        # settings for select mock
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )

        # settings from mosk execute
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.user_token
        self.session.execute.return_value = mock_result

        # settings from mock update
        mock_update.return_value = update(UserTokensTable).where(
            UserTokensTable.user_id == self.user.id
        )

        new_token_value = None

        await update_token(
            user=self.user,
            token=new_token_value,
            token_type=self.token_type,
            db=self.session,
        )

        self.assertEqual(self.user_token.refresh_token, new_token_value)
        self.session.execute.assert_called()
        self.assertEqual(self.session.execute.call_count, 2)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    @patch("src.repository.users.select")
    @patch("src.repository.users.update")
    async def test_update_token_db_err(self, mock_update, mock_select):
        """exceptions database"""
        # settings for select mock
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )

        # settings from mosk execute
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.user_token
        self.session.execute.return_value = mock_result

        # settings from mock update
        mock_update.return_value = update(UserTokensTable).where(
            UserTokensTable.user_id == self.user.id
        )

        self.session.execute.side_effect = Exception("DB error")
        with self.assertRaises(Exception) as context:
            await update_token(
                user=self.user,
                token=self.new_token_value,
                token_type=self.token_type,
                db=self.session,
            )
        self.assertEqual(str(context.exception), "DB error")
        self.session.rollback.assert_called_once()
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    @patch("src.repository.users.select")
    async def test_get_token(self, mock_select):
        """geting token_value"""
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.user_token
        self.session.execute.return_value = mock_result

        result = await get_token(
            user=self.user, 
            token_type=self.token_type, 
            db=self.session
            )
        
        self.assertEqual(result, self.user_token.refresh_token)
        self.session.execute.assert_called_once()

    @patch("src.repository.users.select")
    async def test_get_token_not_found(self, mock_select):
        """token_value not found"""
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mock_result

        result = await get_token(
            user=self.user, 
            token_type=self.token_type, 
            db=self.session
            )
        
        self.assertIsNone(result)
        self.session.execute.assert_called_once()

    @patch("src.repository.users.select")
    async def test_get_token_invalid_token(self, mock_select):
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mock_result

        token_type = "invalid_token"
        result = await get_token(
            user=self.user, 
            token_type=token_type, 
            db=self.session
            )
        self.assertIsNone(result)
        self.session.execute.assert_called_once()

    @patch("src.repository.users.select")
    async def test_get_token_db_error(self, mock_select):
        mock_select.return_value = select(UserTokensTable).filter_by(
            user_id=self.user.id
        )
        self.session.execute.side_effect = Exception("DB error")

        token_type = "refresh_token"
        with self.assertRaises(Exception) as context:
            await get_token(user=self.user, token_type=token_type, db=self.session)

        self.assertEqual(str(context.exception), "DB error")
        self.session.execute.assert_called_once()

    async def test_get_user_by_email(self):
        """get user obj database, use email"""
        # immitation work database
        mocked_user_result = MagicMock()
        mocked_user_result.scalar_one_or_none.return_value = self.user
        self.session.execute.return_value = mocked_user_result

        result = await get_user_by_email(
            email=self.email, 
            db=self.session
            )

        self.assertEqual(result, self.user)
        self.session.execute.assert_called_once()

    @patch("src.repository.users.Gravatar")
    async def test_create_user_success(self, mock_gravatar):
        """
        imitation work Gravatar.

            intercept work Gravatar:
                g = Gravatar(body.email)
                avatar:str = g.get_image() => fake url
        """
        mock_gravatar_instanse = mock_gravatar.return_value
        mock_gravatar_instanse.get_image.return_value = self.new_graw_url

        avatar = mock_gravatar_instanse.get_image()
        self.assertEqual(avatar, self.new_graw_url)

        new_user = UsersTable(**self.test_body.model_dump(), avatar=avatar)
        self.assertEqual(new_user.avatar, avatar)
        self.assertEqual(new_user.email, self.test_body.email)

        result = await create_user(body=self.test_body, db=self.session)

        self.assertEqual(result.avatar, self.new_graw_url)
        self.assertEqual(result.email, self.test_body.email)
        self.assertEqual(result.id, new_user.id)
        self.assertEqual(result.username, new_user.username)
        self.assertEqual(result.password, new_user.password)
        self.assertEqual(result.email, new_user.email)
        self.assertEqual(result.avatar, new_user.avatar)

        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    @patch("src.repository.users.Gravatar.get_image")
    async def create_user_avatar_error(self, mock_get_image):
        """fail request Gravatar" service"""
        mock_get_image.side_effect = Exception("Gtavatar error")

        result = await create_user(
            body=self.test_body, 
            db=self.session
            )

        self.assertIsNone(result.avatar)
        self.assertEqual(result.email, self.test_body.email)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    @patch("src.repository.users.get_user_by_email")
    async def test_confirmed_user_email(self, mock_get_user_by_email):
        """chamge fill confirm=True in user table"""
        mock_get_user_by_email.return_value = self.user

        await confirmed_email(email=self.user.email, db=self.session)

        self.assertTrue(self.user.confirmed)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    @patch("src.repository.users.get_user_by_email")
    async def test_update_user_password(self, mock_get_user_by_email):
        """change fill password=>new_value in user table"""
        mock_get_user_by_email.return_value = self.user

        await update_user_password(
            user=self.user, 
            password=self.new_password, 
            db=self.session
        )

        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertEqual(self.user.password, self.new_password)

    @patch("src.repository.users.get_user_by_email")
    async def test_update_avatar_url(self, mock_get_user_by_email):
        """change fill acatart=>new_url in user table"""
        mock_get_user_by_email.return_value = self.user

        await update_avatar_url(
            email=self.user.email, 
            url=self.new_graw_url, 
            db=self.session
        )

        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertEqual(self.user.avatar, self.new_graw_url)
