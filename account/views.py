from django.shortcuts import render, redirect
from WebApp.settings import EMAIL_HOST_USER
from .models import Faculty_user, FacultyProfile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import AccountAuthenticationForm
from .models import Account
from django.contrib.auth import login, authenticate, logout


def authentication_view(request):
    context = {}
    # print(request)
    # print(request.body)
    # print(request.POST)
    # print(request.META)
    user = request.user
    if user.is_authenticated:
        return redirect("dashboard")

    form = AccountAuthenticationForm(request.POST)
    if request.POST and "loginmain" in str(request.body):
        if form.is_valid():

            email = request.POST["email"]
            password = request.POST["password"]
            # Profile_Photo = request.FILE["profileimg"]
            dept = request.POST["department"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            acc = Account.objects.get(email=email)
            print(acc.role)
            print(str(acc.Department))
            if user is not None:
                if acc.role == (dept).upper():
                    login(request, user)
                    return redirect("dashboard")
            elif user is None:
                return render(
                    request, "account/login_validate.html", {"department": dept}
                )

        else:
            form = AccountAuthenticationForm()

        context["login_form"] = form
        return render(request, "account/auth.html", context)

    elif request.method == "POST":
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        # Profile_Photo = request.FILE.get("profileimg")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password == confirm_password:
            hashed_password = make_password(password)
            log = Faculty_user(
                username=username,
                email=email,
                password=hashed_password,
                phone_number=phone_number,
                # Profile_Photo=Profile_Photo,
                is_active=True,
                role="FACULTY",
            )
            try:
                log.save()
            except Exception as e:
                return render(request, "account/error_message.html", context)
            FacultyProfile.objects.create(user=log, designation="AP", batchlist="0")
            try:
                send_email(username, email)
                context["message"] = (
                    "Registration successful! A confirmation email has been sent."
                )
            except Exception as e:
                context["error"] = (
                    f"Registration successful, but an error occurred while sending the email: {str(e)}"
                )
        else:
            context["error"] = "Passwords do not match."
            return render(request, "account/pass_do_not_match.html", context)

    return render(request, "account/auth.html", context)


def send_email(username, email):
    subject = "Welcome to E-notebook"
    message = f"Hello {username}. Thank You for registering to E-notebook"
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    except Exception as e:
        raise e  # Raise the exception to be caught in the registration_view


def logoutUser(request):
    logout(request)
    return redirect("home")
