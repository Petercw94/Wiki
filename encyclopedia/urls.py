from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newPage", views.newPage, name="newPage"),
    path("wiki/<str:entry>/editPage", views.editPage, name="editPage"),
    path("randomPage", views.randomPage, name="randomPage"),
]
