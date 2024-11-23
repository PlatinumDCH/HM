from django.urls import path
from .apps import QuotesConfig
from . import views
app_name = QuotesConfig.name

urlpatterns = [
    path('', views.home_page,name='home'), #quotes:home
]
