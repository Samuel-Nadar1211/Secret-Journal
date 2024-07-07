from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "event"
urlpatterns = [
    path("", views.home, name="home"),
    path("create", views.create_event, name="create"),
    path("manage", views.manage_event, name="manage"),
    path("<int:event_id>/edit", views.edit_event, name="edit"),
    path("<int:event_id>/remove", views.remove_event, name="remove"),
    path("wish", views.generate_wish, name="generate_wish"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)