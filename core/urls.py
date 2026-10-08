"""
URL configuration for DadBods core public views.
"""

from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("coaches/", views.coaches_view, name="coaches"),
    path("coaching/", views.coaching_view, name="coaching"),
    path("transformations/", views.transformations_view, name="transformations"),
]
