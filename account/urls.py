from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("", views.index, name = "index"),
    path("register", views.register, name = "register"),
    path("logout", views.logout, name = "logout"),
]
