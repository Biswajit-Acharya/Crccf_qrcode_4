import uuid

from django.db import migrations, models


def populate_qr_tokens(apps, schema_editor):
    Employee = apps.get_model("employees", "Employee")
    for employee in Employee.objects.filter(qr_token__isnull=True):
        employee.qr_token = uuid.uuid4()
        employee.save(update_fields=["qr_token"])


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="qr_token",
            field=models.UUIDField(blank=True, null=True, editable=False),
        ),
        migrations.RunPython(populate_qr_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="employee",
            name="qr_token",
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
