from src.services.auth_service import AuthService
from src.services.jwt_service import JWTService
from src.services.password_service import PasswordService
from src.services.user_service import UserService
from src.services.email_service import EmailService

class BasicService:
    password_service = PasswordService()
    jwt_service = JWTService()
    auth_service = AuthService()
    user_setvice = UserService()
    email_service = EmailService()

basic_service = BasicService()