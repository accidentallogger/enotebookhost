from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from .tokens import invite_token_generator
from django.template.loader import render_to_string
from django.contrib import messages
import logging
from account.models import Student_user, StudentProfile
from django.contrib.auth.hashers import make_password
from account.models import FacultyProfile, Faculty_user, Account, Enotebook, experiment
from enotebooktool.models import createNewExperimentInNotebook
from studentInviteStatus.models import Invite
from django.db.models import Q
from enotebooktool.models import experimentData


logger = logging.getLogger(__name__)


@login_required  # Ensures that only logged-in users can send the invite
def send_invite(request):
    if request.method == "POST" and "email_student" in str(request.body):
        email = request.POST.get("student_email")
        batch = request.POST.get("batchno")
        print(email)
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
                "batch": batch,
            },
        )
        try:
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            # Save the invite to the database

            Invite.objects.update_or_create(
                email=email,
                defaults={
                    "supervisor": request.user.username,
                    "token": token,
                    "uid": uid,
                    "status": "Pending",
                },
            )
            messages.success(
                request, "Invite email sent successfully. Check your inbox."
            )
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            messages.error(
                request,
                "There was an error sending the email. Please try again later.",
            )

        return HttpResponse("Invite email sent successfully")
    return render(request, "faculty/final_faculty_dashboard.html")


def student_registration_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError, UnicodeDecodeError) as e:
        print(f"Error decoding uidb64: {e}")
        uid = None

    if uid is not None and invite_token_generator.check_token(uid, token):
        # Token is valid, handle registration logic here
        if request.method == "POST":

            username = f"{request.POST.get('fname')} {request.POST.get('lname')}"
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            profileimg = request.POST.get("profileimg")  # Handle file uploads
            enroll = request.POST.get("enroll")
            department = request.POST.get("department")
            institute = request.POST.get("institute")
            batch = request.POST.get("batchno")
            password = request.POST.get("password")
            confirmpassword = request.POST.get("confirmpassword")

            if password == confirmpassword:
                hashed_password = make_password(password)
                # Create Student User
                student_user = Student_user(
                    username=username,
                    email=email,
                    password=hashed_password,
                    phone_number=phone,
                    Department=department,
                    is_active=True,
                    role="STUDENT",
                )
                student_user.save()

                # Create Student Profile
                information_for_form = request.GET.get(
                    "supervisor", request.user.username
                )
                supervisor = (information_for_form).split("/batch=")[0]
                batchNumber = (information_for_form).split("/batch=")[1]
                StudentProfile.objects.create(
                    user=student_user,
                    enrollment_number=enroll,
                    batch=request.POST.get("batch", batchNumber),
                    supervisorList=request.POST.get(
                        "supervisor", request.user.username
                    ),
                    section="X",
                    is_registered=True,
                )
                try:
                    invite = Invite.objects.get(token=token)
                    print(f"Invite found: {invite}")
                    invite.status = "Accepted"
                    invite.save()
                except Invite.DoesNotExist:
                    print(f"No invite found for Token: {token}")
                    messages.error(request, "Invite not found.")
                    return redirect("home")

                return redirect("auth")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            information_for_form = request.GET.get("supervisor", request.user.username)
            supervisor = (information_for_form).split("/batch=")[0]
            batchNumber = (information_for_form).split("/batch=")[1]
            return render(
                request,
                "dashboard/student_registration.html",
                {"supervisor": supervisor, "batch": batchNumber},
            )
    else:
        messages.error(
            request, "Invalid registration link. Please request a new invitation."
        )
        return redirect("home")


def dashboardview(request):
    user = request.user
    context = {}

    if user.is_authenticated and user.role == "FACULTY":
        facultyview(request, context, user)
        return render(request, "faculty/final_faculty_dashboard.html", context)
    elif user.is_authenticated and user.role == "STUDENT":
        studentuser = request.user
        context = {
            "notes": [i for i in range(1, int(user.totalNotebookCount))],
            "exp-data": [[], [], []],
        }
        acc = Student_user.objects.get(email=user.email)
        if request.method == "POST" and "create-enote" in str(request.body):
            latest = int(user.totalNotebookCount)
            Enotebook.objects.create(account=acc, notebook_number=str(latest + 1))
            user.totalNotebookCount = str(latest + 1)
            user.save()
            context["notes"] = [i for i in range(1, int(user.totalNotebookCount))]
        if request.POST and "enotebook-" in str(request.body):
            con = []
            notebooknumber = str(request.body)
            data = (
                Enotebook.objects.filter(
                    account=user, notebook_number=int(notebooknumber.split("=")[-2].split("-")[-1])
                )
            ).values("id")
            print(data)
            experiment_table_fields = list(
                experiment.objects.filter(enotebook_id=int(data[0]["id"])).values()
            )
            print(experiment_table_fields)
            for expd in experiment_table_fields:
                expData = experimentData.objects.filter(experiment_id=expd["id"])

                con.append(list(expData.values())[0])
                print(con)
            noteid=Enotebook.objects.get(account_id=user.id,notebook_number=notebooknumber.split("=")[-2].split("-")[-1]).id
            print(noteid)
            context = {
                "notes": [i for i in range(1, int(user.totalNotebookCount))],
                "expdata": con,
                "notebooknumber":notebooknumber.split("=")[-2].split("-")[-1],
                "notebookid":noteid,
            }
            print(context)
        if request.POST and "open-notebook-experiment" in str(request.body):
            print(str(request.body))
            newcontext={}
            newcontext["currentExp"]=list(experimentData.objects.filter(id=int((str(request.body))[-3])).values())[0]
            return render(request,"enotebook/main_new.html",newcontext)
        if request.POST and "add-new-experiment-to-notebook" in str(request.body):
            try:
                print(str(request.body))
                noteId=str(request.body).split("=")[-2].split("-")[-1]
                exp = experiment.objects.create(enotebook_id=noteId)
                expdata=experimentData.objects.create(experiment_id=exp.id)
                createNewExperimentInNotebook(expdata)
                newcontext={"notebook_id":noteId,"expID":exp.id,"expdata":expdata}
                return render(request,"enotebook/main_new.html",newcontext)
            except:
                return render(request, "dashboard/final_student_dashboard.html", context)

        return render(request, "dashboard/final_student_dashboard.html", context)
    else:
        return redirect("home")


def facultyview(request, context, user):
    acc = Faculty_user.objects.get(email=user.email)
    batchold = FacultyProfile.objects.get(user=acc).batchlist
    context["batchlist"] = batchold.split(" ")

    if request.method == "POST" and "batch-show-" in str(request.body):
        print(str(request.body))
        try:
            con = []
            studp = StudentProfile.objects.filter(
                batch=(str(request.body)).split("batch-show-")[-1][0]
            ).values()
            for q in studp:
                accn = Student_user.objects.get(id=q["user_id"])
                acc2 = list(Account.objects.filter(email=str(accn)).values())[0]
                student_in_batch = {
                    "studentname": acc2["username"],
                    "studentemail": acc2["email"],
                    "studentphone": acc2["phone_number"],
                }  # need to add image handling ie pfp
                con.append(student_in_batch)
            context["student_in_batch"] = con
            print(context)
            return render(request, "faculty/final_faculty_dashboard.html", context)
        except:
            return redirect(request, "faculty/final_faculty_dashboard.html", context)

    if request.method == "POST" and "batch-submit" in str(request.body):
        b = request.POST.get("batch-name")
        acc = Faculty_user.objects.get(email=user.email)
        old_batch = FacultyProfile.objects.get(user=acc).batchlist
        if b not in old_batch:
            blist = (old_batch) + " " + b
            print(blist)
            faculty = FacultyProfile.objects.get(user=acc)
            faculty.batchlist = blist
            faculty.save()
            context["batchlist"] = blist.split(" ")
            return render(request, "faculty/final_faculty_dashboard.html", context)
