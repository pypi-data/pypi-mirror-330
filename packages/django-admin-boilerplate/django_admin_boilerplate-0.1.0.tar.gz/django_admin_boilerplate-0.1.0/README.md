# Django Admin Boilerplate

🚀 A simple boilerplate for Django admin dashboards with theme settings, user management, and database model overview.

## Features
- 📊 Admin dashboard with dynamic database stats.
- 🎨 User-based theme selection.
- 🔄 Easy integration into existing Django projects.
- 📈 User analytics visualization.

---

## 📦 Installation
1. Install via pip:
   ```sh
   pip install django-admin-boilerplate


2. Add to INSTALLED_APPS in your Django project:
INSTALLED_APPS = [
    "django_admin_boilerplate",
    "django.contrib.admin",
    "django.contrib.auth",
    ...
]


3. Add URLs to urls.py
Modify your project's urls.py to include the admin dashboard:
from django.urls import path, include

urlpatterns = [
    path("admin/", include("django_admin_boilerplate.urls")),
]
