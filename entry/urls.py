from django.urls import path
from . import views

app_name = "entry"
urlpatterns = [
    path("", views.home, name="home"),
    path("create", views.create_entry, name="create"),
    path("<int:entry_id>/read", views.read_entry, name="read"),
    path("<int:entry_id>/edit", views.edit_entry, name="edit"),
    path("<int:entry_id>/remove", views.remove_entry, name="remove"),
]