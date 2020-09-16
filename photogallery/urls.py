from django.urls import path
from . imports views

urlpatterns = [
    path("index/", views.index_randomlist, name="index"),
]