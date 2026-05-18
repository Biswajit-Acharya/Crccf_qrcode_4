import uuid

from django.db import models
from django.urls import reverse


class Employee(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    employee_id = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=120)
    designation = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    phone = models.CharField(max_length=25)
    email = models.EmailField()
    company_name = models.CharField(max_length=180, default="CR Cyber Crime Foundation")
    company_address = models.TextField()
    joining_date = models.DateField()
    profile_photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"

    def get_public_url(self):
        return reverse("employee_public", kwargs={"qr_token": self.qr_token})
