#Django Imports 
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector


#Project File Imports
from .models import Photo, Gallery, Comment, Pinned
from .forms import PhotoForm, GalleryForm, CommentForm


# Views
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
            return redirect(to="view_gallery", gallery_pk=gallery_pk)
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
            gallery.gallery_photos.remove(photo)
            return gallery
        gallery.delete()
        return redirect ("user_galleries")
    return render (request, "photogallery/delete_gallery_and_photos.html", {
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
    photos = Photo.objects.interacted_with().order_by('?').all()[:3]
    all_photos = Photo.objects.public().order_by('?').all()[:5]
    return render(request, "photogallery/index.html", {
        "photos": photos,
        "all_photos": all_photos
    })

def search(request):
    query = request.GET.get("q")
    public_photos = Photo.objects.exclude(public_photo=False)
    public_galleries = Gallery.objects.exclude(public_gallery=False)
    if query is not None:
        galleries = public_galleries.annotate(
            search=SearchVector("title", "gallery_of__username", "photos__camera")
        ).filter(search=query).distinct("title")
        photos = public_photos.annotate(
            search=SearchVector("photo_by__username", "camera", "photo_comments__body")
        ).filter(search=query)
    else:
        galleries = None
        photos = None
    return render(request, "photogallery/search.html", {
        "galleries": galleries,
        "photos": photos,
        "query": query or ""
    })


@login_required
@csrf_exempt
@require_POST
def toggle_fav_photo(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    if photo in request.user.starred_photos.all():
        request.user.starred_photos.remove(photo)
        return JsonResponse({"starred_photo": False})
    else:
        request.user.starred_photos.add(photo)
        return JsonResponse({"starred_photo": True})


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


@login_required
def view_photo(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    photo = Photo.objects.annotate(num_stars=Count("starred_by")).get(pk=photo_pk)
    comments = photo.photo_comments.all()
    starred_photo = False
    if photo in request.user.starred_photos.all():
        starred_photo = True
    return render(request, "photogallery/view_photo.html", {
        "photo": photo,
        "comments": comments,
        "CommentForm": CommentForm,
        "photo_pk": photo_pk,
        "starred_photo": starred_photo
    })