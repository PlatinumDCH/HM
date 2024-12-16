
from django.urls import path
from . import views
from .apps import UserRoomConfig
from django.contrib.auth import views as auth_views

app_name = UserRoomConfig.name

urlpatterns = [
    path('room/', views.register_and_login, name='room'), #users:room
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_pages, name='account'),


#url for reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url='/office/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/office/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    ]
