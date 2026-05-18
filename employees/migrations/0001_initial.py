from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(max_length=40, unique=True)),
                ("full_name", models.CharField(max_length=120)),
                ("designation", models.CharField(max_length=120)),
                ("department", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=25)),
                ("email", models.EmailField(max_length=254)),
                ("company_name", models.CharField(default="CR Cyber Crime Foundation", max_length=180)),
                ("company_address", models.TextField()),
                ("joining_date", models.DateField()),
                ("profile_photo", models.ImageField(blank=True, null=True, upload_to="employee_photos/")),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Inactive", "Inactive")],
                        default="Active",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["full_name"]},
        ),
    ]
