from django.urls import path

from . import views

app_name = "chores"

urlpatterns = [
    path("", views.chore_list, name="chore_list"),
    path("chores/new/", views.chore_create, name="chore_create"),
]
