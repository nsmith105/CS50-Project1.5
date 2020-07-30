from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index")
    path("<str:title>", views.view_page, name="view_page")
]
