from django.apps import AppConfig


class UserRoomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        import users.signals
    # Импортируем signals, чтобы они были зарегистрированы при запуске приложения