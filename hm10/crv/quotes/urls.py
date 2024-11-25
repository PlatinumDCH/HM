from django.urls import path
from .apps import QuotesConfig
from . import views
app_name = QuotesConfig.name

urlpatterns = [
    path('', views.home_page,name='home'), #quotes:home
    path('<int:page>',views.home_page, name='home_paginate'),
    path('search/', views.search, name='search'),  # Добавляем путь для поиска
]
