# CR Cyber Crime Foundation Employee QR Verification

A professional Django web app for managing employee records and verifying employees through stable QR codes.

## Features

- Admin-only login and dashboard.
- Add, edit, delete, search, and filter employees.
- Public read-only employee verification page at `/employee/<employee_id>/`.
- QR codes contain only `/employee/<employee_id>/`, so the QR does not change when employee details are edited.
- JSON API at `/api/employee/<employee_id>/`.
- Browser `localStorage` offline cache for the latest scanned employee details.
- SQLite by default, with settings kept simple for a later MySQL switch.

## File Structure

```text
crccf_qrcode_2/
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── employees/
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
│   └── employees/css/styles.css
├── templates/
│   └── employees/
│       ├── base.html
│       ├── dashboard.html
│       ├── employee_confirm_delete.html
│       ├── employee_form.html
│       ├── login.html
│       └── public_employee.html
├── manage.py
├── requirements.txt
└── README.md
```

## Setup Commands

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Admin dashboard: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login/`
- Django admin: `http://127.0.0.1:8000/django-admin/`
- Public verification example: `http://127.0.0.1:8000/employee/EMP001/`

The account used for this app must be staff or superuser. Non-admin accounts are rejected at login.

## Offline Cache Behavior

When `/employee/<employee_id>/` loads, the browser first fetches `/api/employee/<employee_id>/`.

- If the fetch succeeds, the page renders the latest Django data, saves it to `localStorage` as `employee_<employee_id>`, and shows `Online verified`.
- If the fetch fails, the page checks `localStorage`.
- If cached data exists, it renders the cached data and shows `Offline mode: showing last saved details`.
- If no cached data exists, it shows `Employee data not available offline. Please connect to internet once.`

Django is still the main shared source of truth. `localStorage` is only an offline cache on that one browser/device.
