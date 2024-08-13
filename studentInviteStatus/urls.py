from django.urls import path
from .views import faculty_dashboard_view, resend_invite

urlpatterns = [
    path(
        "student-invite-status/", faculty_dashboard_view, name="faculty_dashboard_view"
    ),
    path("resend-invite/", resend_invite, name="resend_invite"),
]
