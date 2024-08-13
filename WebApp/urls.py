from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("account.urls")),
    path("", include("account.urls")),
    path("password/", include("forgot_password.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("student-stat/", include("studentInviteStatus.urls")),
    path("notebook/", include("enotebooktool.urls")),
]
