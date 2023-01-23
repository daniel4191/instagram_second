from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'), # /accounts/login/ => settings.LOGIN_URL
    path('logout/', views.logout, name = 'logout')
]