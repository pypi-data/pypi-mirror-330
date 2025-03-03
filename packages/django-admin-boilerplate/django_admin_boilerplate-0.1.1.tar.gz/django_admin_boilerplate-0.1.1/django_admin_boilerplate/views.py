from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.contrib.auth.models import User
from .models import ThemeSetting  # Ensure ThemeSetting is imported

from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.db import models  # ✅ Import models
import json

User = get_user_model()

# Helper function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# Admin Login View
def admin_login(request):
    user_theme = "default"
    if request.user.is_authenticated:
        user_theme = ThemeSetting.objects.filter(user=request.user).values_list("theme", flat=True).first() or "default"

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")

    return render(request, "admin_boilerplate/admin_login.html", {"user_theme": user_theme})


# Admin Logout
def admin_logout(request):
    logout(request)
    return redirect("admin_login")


# Admin Dashboard
@user_passes_test(is_admin, login_url="admin_login")
def admin_dashboard(request):
    user_theme = ThemeSetting.objects.filter(user=request.user).values_list("theme", flat=True).first() or "default"
    models_data = {}

    for model in apps.get_models():
        model_name = model.__name__
        fields = [field.name for field in model._meta.get_fields()]
        records = model.objects.count()  # Get record count instead of listing all data
        
        models_data[model_name] = {"fields": fields, "count": records}

    user_count = User.objects.count()

    return render(request, "admin_boilerplate/admin_dashboard.html", {
        "models_data": models_data,
        "user_count": user_count,
        "user_theme": user_theme,  # Pass theme to template
    })



@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def users_page(request):
    user_theme = ThemeSetting.objects.filter(user=request.user).values_list("theme", flat=True).first() or "default"

    # Get user count per month
    user_counts_by_month = (
        User.objects.annotate(month=models.functions.ExtractMonth("date_joined"))
        .values("month")
        .annotate(count=models.Count("id"))
        .order_by("month")
    )

    # Convert data for JavaScript chart
    months = [entry["month"] for entry in user_counts_by_month]
    user_counts = [entry["count"] for entry in user_counts_by_month]

    return render(request, "admin_boilerplate/users.html", {
        "user_theme": user_theme,
        "months": json.dumps(months),
        "user_counts": json.dumps(user_counts),
    })




@user_passes_test(is_admin, login_url="admin_login")
@login_required
def change_theme(request, theme_name):
    theme, created = ThemeSetting.objects.get_or_create(user=request.user)
    theme.theme = theme_name
    theme.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
