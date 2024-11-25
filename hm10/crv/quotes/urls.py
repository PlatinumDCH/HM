from django.urls import path
from .apps import QuotesConfig
from . import views

app_name = QuotesConfig.name

urlpatterns = [
    path('', views.home_page,name='home'), #quotes:home
    path('<int:page>',views.home_page, name='home_paginate'),
    path('search/', views.search, name='search'),
    path('author/<int:id>/', views.author_detail, name='author_detail'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
]
