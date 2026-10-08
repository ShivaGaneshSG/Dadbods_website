"""
URL patterns for Coaching Applications.
"""

from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/", views.apply_view, name="apply"),
    path("apply/success/", views.application_success_view, name="success"),
    path("dashboard/", views.admin_dashboard_summary_view, name="admin_dashboard"),
]
