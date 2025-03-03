from django.urls import path
from .views import admin_login, admin_logout, admin_dashboard, change_theme, users_page

urlpatterns = [
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-logout/", admin_logout, name="admin_logout"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("users/", users_page, name="users_page"),


    path('change-theme/<str:theme_name>/', change_theme, name='change_theme'),
]
