from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin
from account.models import Account, FacultyProfile, StudentProfile


class AccountAdmin(admin.ModelAdmin):
    list_display = ["role", "phone_number", "email", "date_joined", "last_login"]
    search_fields = ["phone_number", "email", "username", "role"]
    readonly_fields = ["date_joined", "last_login"]
    filter_horizontal = []
    list_filter = []
    fieldsets = []


class AccountAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "email", "date_joined", "last_login"]
    search_fields = ["phone_number", "email", "username"]
    readonly_fields = ["date_joined", "last_login"]
    filter_horizontal = []
    list_filter = []
    fieldsets = []


admin.site.register(Account, AccountAdmin)
