from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from cloudinary.models import CloudinaryField


class accountmanager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Users must have email")
        if not username:
            raise ValueError("Users must have username")
        user = self.model(
            email=self.normalize_email(email), username=username, **extra_fields
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        FACULTY = "FACULTY", "Faculty"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField()
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    Profile_Photo = CloudinaryField("image", null=True, blank=True)
    Department = models.CharField(max_length=50)

    class genderchoose(models.Model):
        GENDER_CHOICES = (
            ("M", "Male"),
            ("F", "Female"),
        )

    gender = models.CharField(
        max_length=1, choices=genderchoose.GENDER_CHOICES, default="F"
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.",
    )
    phone_number = models.CharField(
        # Validators should be a list
        validators=[phone_regex],
        max_length=12,
        blank=True,
    )
    totalNotebookCount = models.CharField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number", "role"]

    objects = accountmanager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


###########
class StudentProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    batch = models.CharField(default=1, null=True)
    enrollment_number = models.CharField(unique=True, null=True, blank=True)
    section = models.CharField(blank=True)
    supervisorList = models.CharField(blank=True)
    Profile_Photo = CloudinaryField("image", null=True, blank=True)
    is_registered = models.BooleanField(default=False)


class StudentManager(accountmanager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Account.Role.STUDENT)


class Student_user(Account):
    base_role = Account.Role.STUDENT
    objects = StudentManager()

    @property
    def Studentmorepfp(self):
        return self.StudentProfile

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Account.Role.STUDENT
        return super().save(*args, **kwargs)


############
class FacultyProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    designation = models.CharField(max_length=30)
    batchlist = models.CharField(default="0")


class FacultyManager(accountmanager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Account.Role.FACULTY)


class Faculty_user(Account):
    base_role = Account.Role.FACULTY
    objects = FacultyManager()

    @property
    def Facultymorepfp(self):
        return self.FacultyProfile

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Account.Role.FACULTY
        return super().save(*args, **kwargs)


class Enotebook(models.Model):
    notebook_number = models.CharField(null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class experiment(models.Model):
    experiment_number = models.CharField()
    enotebook = models.ForeignKey(Enotebook, on_delete=models.CASCADE)
