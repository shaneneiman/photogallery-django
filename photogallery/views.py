#Django Imports 
from django.shortcuts import render, redirect, get_object_or_404

#Project File Imports
from .models import Photo

# Create your views here.
def add_gallery(request):
    pass


def add_photo(request):
    pass


def delete_gallery(request):
    pass


def delete_photo(request):
    pass


def edit_gallery(request):
    pass


def index_randomlist(request):
    # Later add annotate to only display photos that are public 
    # and have a comments or are starred.
    # Limit display to 15 photos?
    photos = Photo.objects.all()
    return render(request, "photogallery/index.html")


def user_galleries_list(request):
    pass


def user_photos_list(request):
    pass