from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        "password-reset/", views.password_reset_request, name="password_reset_request"
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/auth.html"),
        name="login",
    ),
]
