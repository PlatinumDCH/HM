
from django.urls import path
from . import views
from .apps import UserRoomConfig

app_name = UserRoomConfig.name

urlpatterns = [
    path('room/', views.register_and_login, name='room'), #users:room
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_pages, name='account'),
]
