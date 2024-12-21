import unittest
from unittest.mock import AsyncMock, MagicMock
from mock_alchemy.mocking import AlchemyMagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.conection_postgres import DatabaseSessionManager
from src.database.conection_postgres import get_connection_db
from src.database.conection_postgres import sessionmanager

class test_get_connection_db(unittest.IsolatedAsyncioTestCase):

    async def test_get_connection_db(self):

        mock_session = AlchemyMagicMock(spec=AsyncSession)
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None

        # Мокаем sessionmanager.session
        with unittest.mock.patch.object(sessionmanager, "session", return_value=mock_session_context):
            # Используем асинхронный генератор
            async for session in get_connection_db():
                # Проверяем, что возвращается мок сессии
                self.assertEqual(session, mock_session)

            # Проверяем, что контекстный менеджер завершил работу
            mock_session_context.__aexit__.assert_called_once()

            # Проверяем, что сессия была закрыта
            mock_session.close.assert_called_once()