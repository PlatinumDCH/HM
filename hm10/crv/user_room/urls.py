
from django.urls import path
from . import views
from .apps import UserRoomConfig

app_name = UserRoomConfig.name

urlpatterns = [
    path('room/', views.register_and_login, name='room'), #user_room:room
]
