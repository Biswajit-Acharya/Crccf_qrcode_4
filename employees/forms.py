from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Employee


class AdminAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not (user.is_staff or user.is_superuser):
            raise forms.ValidationError("Only administrator accounts can access this system.", code="not_admin")


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "full_name",
            "designation",
            "department",
            "phone",
            "email",
            "company_name",
            "company_address",
            "joining_date",
            "profile_photo",
            "status",
        ]
        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
            "company_address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"].strip()
        if not employee_id:
            raise forms.ValidationError("Employee ID is required.")
        return employee_id
