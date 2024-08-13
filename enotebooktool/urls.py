from django.urls import path
from enotebooktool import views


urlpatterns = [
    path("", views.notebookview, name="notebook"),
]
