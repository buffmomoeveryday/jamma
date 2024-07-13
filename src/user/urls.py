from django.urls import path

from .views import login, logout, register_user

urlpatterns = [
    path("login", login, name="login"),
    path("register", register_user, name="register"),
    path("logout", logout, name="logout"),
]
