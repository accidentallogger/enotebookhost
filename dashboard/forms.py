from django import forms
from account.models import Account


class InviteCodeForm(forms.Form):
    email = forms.EmailField(label="Student Email")


# class StudentRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ["name", "email"]
