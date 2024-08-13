from django.urls import path
from dashboard import views


urlpatterns = [
    path("", views.dashboardview, name="dashboard"),
    path("send_invite/", views.send_invite, name="send_invite"),
    path(
        "student_registration/<str:uidb64>/<str:token>/",
        views.student_registration_view,
        name="student_registration_view",
    ),
]
