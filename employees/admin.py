from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "designation", "department", "status", "updated_at")
    list_filter = ("status", "department")
    search_fields = ("employee_id", "full_name", "email", "phone")
    readonly_fields = ("created_at", "updated_at")
