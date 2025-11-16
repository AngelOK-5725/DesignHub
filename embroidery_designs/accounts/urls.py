# embroidery_designs/accounts/urls.py  

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),


    path('password-reset/', auth_views.PasswordResetView.as_view(), 
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),
]
