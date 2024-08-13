from django.urls import path
from django.contrib.auth import views as auth_views
from account import views


urlpatterns = [
    path("", views.authentication_view, name="auth"),
    path("", views.authentication_view, name="home"),
    path("logout_user", views.logoutUser, name="logout"),
]
