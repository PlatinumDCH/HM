from unittest.mock import Mock
import pytest

from tests.conftest import TestingSessionLocal
# from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.users import get_user_by_email
# from src.schemas import UserSchema
# from src.entity.models import UsersTable


from main import app



user_data={
    "username": "test_agent", 
    "email": "test_agent@example.com", 
    "password": "123456789"
    }

def test_signup(client, monkeypatch):
    mock_send_mail = Mock()
    monkeypatch.setattr(
        'src.services.email_service.EmailService.send_email', mock_send_mail)
    headers = {"User-Agent": "TestClient"}
    response = client.post(
        'api/auth/signup',
        json=user_data,
        headers=headers

    )
    assert response.status_code == 201, response.text


