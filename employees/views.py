from io import BytesIO

import qrcode
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import EmployeeForm
from .models import Employee


def pwa_manifest(request):
    manifest_path = settings.BASE_DIR / "static" / "manifest.json"
    return FileResponse(open(manifest_path, "rb"), content_type="application/manifest+json")


def service_worker(request):
    worker_path = settings.BASE_DIR / "static" / "employees" / "js" / "service-worker.js"
    response = HttpResponse(open(worker_path, encoding="utf-8").read(), content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    return response


def admin_required(view_func):
    @login_required
    @user_passes_test(lambda user: user.is_staff or user.is_superuser)
    def wrapped(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped


@admin_required
def dashboard(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    employees = Employee.objects.all()

    if query:
        employees = employees.filter(Q(employee_id__icontains=query) | Q(full_name__icontains=query))

    if status in {Employee.Status.ACTIVE, Employee.Status.INACTIVE}:
        employees = employees.filter(status=status)

    return render(
        request,
        "employees/dashboard.html",
        {"employees": employees, "query": query, "status": status},
    )


@admin_required
def employee_create(request):
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        employee = form.save()
        messages.success(request, f"Employee {employee.employee_id} added successfully.")
        return redirect("dashboard")
    return render(request, "employees/employee_form.html", {"form": form, "title": "Add Employee"})


@admin_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=employee)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Employee {employee.employee_id} updated successfully.")
        return redirect("dashboard")
    return render(request, "employees/employee_form.html", {"form": form, "title": "Edit Employee"})


@admin_required
@require_http_methods(["GET", "POST"])
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect("dashboard")
    return render(request, "employees/employee_confirm_delete.html", {"employee": employee})


@admin_required
def employee_qr_download(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    qr = qrcode.QRCode(box_size=10, border=4)
    verification_url = request.build_absolute_uri(f"/v/{employee.qr_token}/")
    qr.add_data(verification_url)

    qr.make(fit=True)
    image = qr.make_image(fill_color="#08284a", back_color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    filename = f"{employee.employee_id}_qr.png"
    return FileResponse(buffer, as_attachment=True, filename=filename, content_type="image/png")


def employee_scanner(request):
    return render(request, "employees/scanner.html")


def employee_public(request, qr_token):
    api_path = reverse("employee_api", kwargs={"qr_token": qr_token})
    return render(
        request,
        "employees/public_employee.html",
        {"lookup_key": str(qr_token), "api_url": api_path},
    )


def employee_verify(request, token):
    employee = get_object_or_404(Employee, qr_token=token)
    return render(request, "employees/employee_verify.html", {"employee": employee})


def employee_public_by_employee_id(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    return redirect("employee_public", qr_token=employee.qr_token)


def serialize_employee(request, employee):
    photo_url = request.build_absolute_uri(employee.profile_photo.url) if employee.profile_photo else ""
    return {
        "employee_id": employee.employee_id,
        "full_name": employee.full_name,
        "designation": employee.designation,
        "department": employee.department,
        "phone": employee.phone,
        "email": employee.email,
        "company_name": employee.company_name,
        "company_address": employee.company_address,
        "joining_date": employee.joining_date.isoformat(),
        "profile_photo": photo_url,
        "status": employee.status,
        "verification_status": "Verified Employee"
        if employee.status == Employee.Status.ACTIVE
        else "Inactive Employee",
        "updated_at": employee.updated_at.isoformat(),
    }


def employee_api(request, qr_token):
    employee = get_object_or_404(Employee, qr_token=qr_token)
    return JsonResponse(serialize_employee(request, employee))


def employee_api_by_employee_id(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    return JsonResponse(serialize_employee(request, employee))
