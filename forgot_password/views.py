from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from decouple import config
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)

                    email_subject = "Password Reset Request"
                    email_body = render_to_string(
                        "forgot_password/reset_password_email.html",
                        {
                            "user": user,
                            "domain": request.get_host(),
                            "uid": uid,
                            "token": token,
                        },
                    )
                    try:
                        send_mail(
                            email_subject,
                            email_body,
                            settings.DEFAULT_FROM_EMAIL,
                            [email],
                        )
                        messages.success(
                            request, "Password reset email sent. Check your inbox."
                        )
                    except Exception as e:
                        logger.error(f"Failed to send email to {email}: {e}")
                        messages.error(
                            request,
                            "There was an error sending the email. Please try again later.",
                        )
            else:
                messages.error(request, "No user found with this email address.")
                return redirect("password_reset_request")

            return redirect("password_reset_request")

    else:
        form = PasswordResetForm()

    return render(
        request, "forgot_password/password_reset_request.html", {"form": form}
    )


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Password reset successful. You can now log in with your new password.",
                )
                return redirect("login")
        else:
            form = SetPasswordForm(user)

        return render(
            request, "forgot_password/password_reset_confirm.html", {"form": form}
        )
    else:
        messages.error(request, "Invalid password reset link.")
        return redirect("login")
