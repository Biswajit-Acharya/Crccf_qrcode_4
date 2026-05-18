from django.urls import path

from . import views


urlpatterns = [
    path("employees/add/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/edit/", views.employee_update, name="employee_update"),
    path("employees/<int:pk>/delete/", views.employee_delete, name="employee_delete"),
    path("employees/<int:pk>/qr/", views.employee_qr_download, name="employee_qr_download"),
    path("scanner/", views.employee_scanner, name="employee_scanner"),
    path("employee/<uuid:qr_token>/", views.employee_public, name="employee_public"),
    path("employee/id/<str:employee_id>/", views.employee_public_by_employee_id, name="employee_public_by_employee_id"),
    path("api/employee/<uuid:qr_token>/", views.employee_api, name="employee_api"),
    path("api/employee/id/<str:employee_id>/", views.employee_api_by_employee_id, name="employee_api_by_employee_id"),
]
