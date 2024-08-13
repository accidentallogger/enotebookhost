from django.shortcuts import render, redirect
from account.models import StudentProfile
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from dashboard.tokens import invite_token_generator
from django.template.loader import render_to_string
from .models import Invite
from account.models import StudentProfile
import logging

logger = logging.getLogger(__name__)


# @login_required  # Ensure only logged-in faculty can access this


def faculty_dashboard_view(request):
    invites = Invite.objects.all()
    return render(request, "faculty/student_inv_status.html", {"invites": invites})


def resend_invite(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            token = invite_token_generator.make_token(email)
            uid = urlsafe_base64_encode(force_bytes(email))
            email_subject = "Your Invite Link"
            email_body = render_to_string(
                "dashboard/student_registration_email.html",
                {
                    "email": email,
                    "domain": request.get_host(),
                    "uid": uid,
                    "token": token,
                    "supervisor": request.user.username,
                },
            )
            try:
                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return JsonResponse(
                    {"message": "Invite email resent successfully"}, status=200
                )
            except Exception as e:
                logger.error(f"Failed to resend email to {email}: {e}")
                return JsonResponse(
                    {"message": "Error resending invite email"}, status=500
                )
    return JsonResponse({"message": "Invalid request"}, status=400)
