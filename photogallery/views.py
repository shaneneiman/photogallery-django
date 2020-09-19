#Django Imports 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

#Project File Imports
from .models import Photo, Gallery, Comment, Pinned
from .forms import PhotoForm, GalleryForm, CommentForm

# Create your views here.
@login_required
def add_comment(request, photo_pk):
    if request.method == "GET":
        form = CommentForm()
    else:
        photo = get_object_or_404(Photo, pk=photo_pk)
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.comment_by = request.user
            comment.comments = photo
            comment.save()
            return redirect(to="view_photo", photo_pk=photo_pk)
    return render(request, "photogallery/add_comment.html", {
        "form": form
    })


@login_required
def add_gallery(request):
    if request.method == "GET":
        form = GalleryForm()
    else:
        form = GalleryForm(request.POST, files=request.FILES)
        if form.is_valid:
            gallery = form.save()
            gallery.gallery_of.add(request.user)
            gallery.save()
            return redirect(to="view_gallery", gallery_pk=gallery.pk)
    return render(request, "photogallery/add_gallery.html", {
        "form": form
    })


@login_required
def add_photo(request):
    if request.method =="GET":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, files=request.FILES)
        if form.is_valid:
            photo = form.save(commit=False)
            photo.photo_by = request.user
            photo.save()
            return redirect(to="user_photos")
    return render(request, "photogallery/add_photo.html", {
        "form": form
    })


@login_required
def add_photo_to_gallery(request, gallery_pk):
    if request.method == "GET":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, files=request.FILES)
        gallery = get_object_or_404(Gallery, pk=gallery_pk)
        if form.is_valid:
            photo = form.save(commit=False)
            photo.photo_by = request.user
            photo.save()
            photo.gallery_photos.add(gallery)
            photo.save()
            return redirect(to="view_gallery", question_pk=question_pk)
    return render(request, "photogallery/add_photo_to_gallery.html", {
        "form": form
    })



@login_required
def delete_gallery(request, gallery_pk):
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    if request.method == "POST":
        gallery.delete()
        return redirect ("user_galleries")
    return render (request, "photogallery/delete_gallery.html", {
        "gallery": gallery
    })


@login_required
def delete_gallery_and_photos(request, gallery_pk):
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    if request.method == "POST":
        for photo in gallery.gallery_photos.all():
            photo.delete()
            return gallery
        gallery.delete()
        return redirect ("user_galleries")
    return render (request, "photogallery/delete_gallery.html", {
        "gallery": gallery
    })


@login_required
def delete_photo(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    if request.method == "POST":
        photo.delete()
        return redirect ("user_photos")
    return render (request, "photogallery/delete_photo.html", {
        "photo": photo
    })


@login_required
def edit_gallery(request):
    pass


def index_randomlist(request):
    photos = Photo.objects.interacted_with
    return render(request, "photogallery/index.html", {
        "photos": photos
    })


@login_required
def user_galleries_list(request):
    galleries = request.user.gallery_users.all()
    return render(request, "photogallery/user_galleries_list.html", {
        "galleries": galleries
    })


@login_required
def user_photos_list(request):
    photos = request.user.user_photos.all()
    return render(request, "photogallery/user_photos_list.html", {
        "photos": photos
    })


def view_gallery(request, gallery_pk):
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    photos = gallery.photos.all()
    return render(request, "photogallery/view_gallery.html", {
        "gallery": gallery,
        "photos": photos,
        "PhotoForm": PhotoForm,
        "gallery_pk": gallery_pk
    })


def view_photo(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    comments = photo.photo_comments.all()
    return render(request, "photogallery/view_photo.html", {
        "photo": photo,
        "comments": comments,
        "CommentForm": CommentForm,
        "photo_pk": photo_pk
    })