from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("home/", views.home, name="home"),
    path("home/client/", views.client, name="client"),
    path("home/personnel/", views.personnel, name="personnel"),
    path("home/client/<int:pk>", views.get_client, name="get_client"),
    path("home/client/add", views.add_client, name="add_client"),
    path("home/client/added", views.added_client, name="added_client"),
    path("home/client/edit", views.edit, name="edit"),
    path("home/client/delete", views.delete, name="delete"),
]
