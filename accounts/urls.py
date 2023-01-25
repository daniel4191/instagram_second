from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'), # /accounts/login/ => settings.LOGIN_URL
    path('logout/', views.logout, name = 'logout'),
    path('edit/', views.profile_edit, name = 'profile_edit'),
    path('password_change/', views.password_change, name = 'password_change')
]