from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="title"),
    path("search", views.search, name="search"),
    path("rando", views.rando, name="rando"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit")
]
