from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random-page", views.random_page, name="random page"),
    path("add_page", views.add_page, name="add_page"),
    path("<str:title>", views.title, name="title"),
    path("<str:entry>/edit", views.edit, name="edit")
    
]
